import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser(description="Check Soda's repeated owner-state decision gate.")
parser.add_argument('--soda', type=Path, required=True, help='Path to the Soda 1.4.0 CLI with Composer dependencies installed.')
args = parser.parse_args()
cli = args.soda.resolve()

with tempfile.TemporaryDirectory(prefix='soda-gate-') as directory:
    root = Path(directory)
    config = root / 'soda.php'
    config.write_text('''<?php
return \\Cosmira\\Soda\\Config\\Soda::configure()->with([
    new \\Cosmira\\Soda\\Rules\\Design\\RepeatedForeignStateDecision,
]);
''')
    for case, expected in [('repeated', 1), ('encapsulated', 0)]:
        case_directory = root / case
        case_directory.mkdir()
        source = case_directory / 'example.php'
        owner = 'class Post { public bool $published = true; public bool $deleted = false;'
        expression = '$post->published && ! $post->deleted'
        if case == 'encapsulated':
            owner += ' public function isVisible(): bool { return $this->published && ! $this->deleted; }'
            expression = '$post->isVisible()'
        consumers = '\n'.join(f'function {name}(Post $post): bool {{ return {expression}; }}' for name in ['show', 'notify', 'index'])
        source.write_text('<?php\n' + owner + ' }\n' + consumers + '\n')
        report = root / f'{case}.json'
        command = ['php', str(cli), 'quality', str(case_directory), f'--config={config}', '--report-type=json', f'--report-file={report}']
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != expected:
            raise AssertionError(f'{case}: expected exit {expected}, got {result.returncode}\n{result.stdout}\n{result.stderr}')
        if not report.exists():
            raise AssertionError(f'{case}: no JSON report\n{result.stdout}\n{result.stderr}')
        data = json.loads(report.read_text())
        rules = [violation['rule'] for violation in data['violations']]
        if rules != (['repeated_foreign_state_decision'] if expected else []):
            raise AssertionError(f'{case}: unexpected diagnostics {rules}')
        print(f'{case}: exit {result.returncode}, rules={rules}')
