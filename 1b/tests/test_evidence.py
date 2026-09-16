"""Regression checks for publication verification; no credentials or network."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from verify_evidence import digest, prompt_from_file, verify_api_run


class EvidenceChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.run = self.project / 'run'
        self.run.mkdir()
        self.item = self.project / 'item.md'
        self.item.write_text('---\nid: item\n---\n\n## Prompt\nQuestion only.\n\n## Rubric\nDo not send this.\n')
        h = digest('Question only.')
        self.manifest = {'items': [{'id': 'item', 'path': 'item.md', 'prompt': 'Question only.', 'prompt_sha256': h}],
                         'models': ['test/model'], 'arguments': {'n': 2, 'reasoning_effort': 'high', 'max_tokens': 100}}
        self.rows = [{'item': 'item', 'model': 'test/model', 'sample': n, 'prompt_sha256': h,
                      'content': f'Answer {n}', 'requested_reasoning_effort': 'high', 'max_tokens': 100,
                      'finish_reason': 'stop', 'error': None} for n in range(2)]
        self.audits = [{**r, 'answer': r['content'], 'target_grade': 'pass'} for r in self.rows]

    def write(self):
        for name, value in [('manifest', self.manifest), ('manual_audit', {'records': self.audits}),
                            ('summary', {'records': 2, 'valid': 2})]:
            (self.run / (name + '.json')).write_text(json.dumps(value))
        (self.run / 'raw.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in self.rows))

    def test_prompt_excludes_rubric_and_out_of_order_samples_pass(self):
        self.assertEqual(prompt_from_file(self.item), 'Question only.')
        self.rows.reverse()
        self.write()
        self.assertEqual(len(verify_api_run(self.run, self.project)[0]), 2)

    def test_missing_and_duplicate_samples_rejected(self):
        original = copy.deepcopy(self.rows)
        for replacement in [original[:1], [original[0], original[0]]]:
            with self.subTest(replacement=replacement):
                self.rows = replacement
                self.write()
                with self.assertRaises(ValueError):
                    verify_api_run(self.run, self.project)

    def test_changed_answer_rejected(self):
        self.rows[0]['content'] = 'Changed after audit'
        self.write()
        with self.assertRaisesRegex(ValueError, 'answer/audit mismatch'):
            verify_api_run(self.run, self.project)

    def test_changed_prompt_rejected(self):
        self.item.write_text('## Prompt\nDifferent question.\n')
        self.write()
        with self.assertRaisesRegex(ValueError, 'changed prompt'):
            verify_api_run(self.run, self.project)

    def test_truncated_answer_cannot_count_as_pass(self):
        self.rows[0]['finish_reason'] = 'length'
        self.write()
        with self.assertRaisesRegex(ValueError, 'incomplete response'):
            verify_api_run(self.run, self.project)


if __name__ == '__main__':
    unittest.main()
