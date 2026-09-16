#!/usr/bin/env python3
"""Check published records offline; summarize existing author-agent grades."""

import hashlib
import json
from collections import Counter
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def prompt_from_file(path):
    match = re.search(r'^## Prompt\n(.*?)(?=^## |\Z)', path.read_text(), re.S | re.M)
    require(match is not None and match.group(1).strip(), f'{path}: missing prompt')
    return match.group(1).strip()


def keyed(records, label):
    keys = [(r['item'], r['model'], r['sample']) for r in records]
    require(len(keys) == len(set(keys)), f'{label}: duplicate sample tuple')
    return dict(zip(keys, records))


def verify_api_run(run, project):
    manifest = read_json(run / 'manifest.json')
    audits = read_json(run / 'manual_audit.json')['records']
    rows = [json.loads(line) for line in (run / 'raw.jsonl').read_text().splitlines() if line.strip()]
    raw_by_key = keyed(rows, run.name)
    audit_by_key = keyed(audits, run.name + ' audit')
    items = manifest['items']
    require(len({item['id'] for item in items}) == len(items), f'{run.name}: duplicate item ID')
    hashes = {}
    for item in items:
        path = (project / item['path']).resolve()
        require(project.resolve() in path.parents, f'{run.name}: item path outside project')
        prompt = prompt_from_file(path)
        require(prompt == item['prompt'], f'{run.name}: changed prompt {item["id"]}')
        require(digest(prompt) == item['prompt_sha256'], f'{run.name}: manifest hash mismatch')
        hashes[item['id']] = item['prompt_sha256']
    expected = {(item['id'], model, sample) for item in items
                for model in manifest['models'] for sample in range(manifest['arguments']['n'])}
    require(set(raw_by_key) == expected, f'{run.name}: missing or unexpected samples')
    require(set(audit_by_key) == expected, f'{run.name}: audit sample coverage mismatch')
    for key, row in raw_by_key.items():
        audit = audit_by_key[key]
        require(row['prompt_sha256'] == audit['prompt_sha256'] == hashes[row['item']],
                f'{run.name}: record prompt hash mismatch {key}')
        require(row['content'] == audit['answer'], f'{run.name}: answer/audit mismatch {key}')
        require(row['requested_reasoning_effort'] == manifest['arguments']['reasoning_effort'],
                f'{run.name}: effort mismatch {key}')
        require(row['max_tokens'] == manifest['arguments']['max_tokens'],
                f'{run.name}: token setting mismatch {key}')
        invalid = bool(row.get('error')) or not row['content'].strip() or row.get('finish_reason') in {
            'length', 'content_filter', 'error'}
        require(not invalid or audit['target_grade'] == 'excluded',
                f'{run.name}: incomplete response counted as substantive {key}')
    summary = read_json(run / 'summary.json')
    require(summary['records'] == len(rows), f'{run.name}: summary count mismatch')
    require(summary['valid'] == sum(r['target_grade'] != 'excluded' for r in audits),
            f'{run.name}: summary valid count mismatch')
    return rows, audits


def verify_codex_run(run, project):
    audit = read_json(run / 'manual_audit.json')
    records = audit['records']
    # In these historical audits, n counts items; each has one _s0 answer.
    require(audit['n'] == len(records), f'{run.name}: audit item count mismatch')
    require(len({r['item'] for r in records}) == len(records), f'{run.name}: duplicate item')
    require({p.name for p in run.glob('*_s*.md')} == {f'{r["item"]}_s0.md' for r in records},
            f'{run.name}: missing or unexpected Codex answer files')
    for row in records:
        paths = list((project / 'questions').glob(f'*/{row["item"]}.md'))
        require(len(paths) == 1, f'{run.name}: question missing or ambiguous')
        prompt = prompt_from_file(paths[0])
        require(prompt == row['prompt'] and digest(prompt) == row['prompt_sha256'],
                f'{run.name}: question/hash mismatch')
        answer = (run / f'{row["item"]}_s0.md').read_text().strip()
        require(answer == row['answer'].strip(), f'{run.name}: answer/audit mismatch')
    require(audit['conceptual_pass'] == sum(r['conceptual_grade'] == 'pass' for r in records),
            f'{run.name}: pass count mismatch')
    return records


def verify_checksums(repo):
    checksums = read_json(repo / 'evidence_checksums.json')
    for rel, expected in checksums.items():
        path = repo / rel
        require(path.is_file(), f'Missing published file: {rel}')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, f'Changed published file: {rel}')
    return len(checksums)


def main():
    checked = verify_checksums(REPO)
    published = read_json(REPO / 'evidence_checksums.json')
    project = REPO / '1b'
    roots = sorted((project / 'tests/results').iterdir())
    print('# Published evidence verification\n')
    print('Offline consistency checks only. Grades below are author-agent judgments, not independent regrading.\n')
    print('| Run | Records | Main passes | Main failures | Excluded | Other judgments |')
    print('| --- | ---: | ---: | ---: | ---: | --- |')
    total = 0
    confirmations = []
    run_count = 0
    for run in roots:
        if not run.is_dir() or not (run / 'manual_audit.json').exists():
            continue
        # Only the published snapshot is verified; unreviewed new runs stay local.
        if str((run / 'manual_audit.json').relative_to(REPO)) not in published:
            continue
        run_count += 1
        if (run / 'raw.jsonl').exists():
            rows, audits = verify_api_run(run, project)
            grades = Counter(r['target_grade'] for r in audits)
            count = len(rows)
            if run.name in {'support_confirm_deepseek_high_20260917', 'explanation_confirm_high_20260917'}:
                confirmations.extend(audits)
        else:
            records = verify_codex_run(run, project)
            count = len(records)
            grades = Counter(r['conceptual_grade'] for r in records)
        total += count
        other = ', '.join(f'{name}: {n}' for name, n in sorted(grades.items())
                          if name not in {'pass', 'fail', 'excluded'}) or 'none'
        print(f'| {run.name} | {count} | {grades["pass"]} | {grades["fail"]} | {grades["excluded"]} | {other} |')
    pages = read_json(project / 'submission/1b_native_pages.json')
    for page, item in zip(pages[1:4], ['b25-01', 'b25-04', 'b26-05']):
        question = next(text for heading, text in page['sections'] if heading == 'Question')
        path = next((project / 'questions').glob(f'*/{item}.md'))
        require(question == prompt_from_file(path), f'Submission changed tested question: {item}')
    composed = []
    for page in pages:
        composed.append('# ' + page['title'])
        for heading, text in page['sections']:
            composed.extend(['## ' + heading, text])
    require('\n\n'.join(composed) + '\n' == (project / 'submission/1b_submission.md').read_text(),
            'Markdown and composition JSON disagree')
    print('\n## Explanation grades in selected confirmations\n')
    print('These categories are separate from the main-verdict counts above. Borderline categories are not decisive errors.\n')
    print('| Item | Model | Explanation/repair grade | Count |')
    print('| --- | --- | --- | ---: |')
    groups = Counter((r['item'], r['model'], r['explanation_grade']) for r in confirmations)
    for (item, model, grade), count in sorted(groups.items()):
        print(f'| {item} | {model} | {grade} | {count} |')
    print(f'\nVerified {checked} files, {run_count} runs and {total} answer records. All three submission questions match the tested prompts.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, StopIteration) as exc:
        print(f'VERIFICATION FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
