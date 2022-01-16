import itertools
import json
import typing

import loguru

data_path = 'trace_runs.json'


def grouped_data_by_target(data: typing.Iterator[dict]) -> dict[str, list[dict]]:
    """
    Group data by target.
    """
    grouped_data = {}
    for d in data:
        target = d['target']
        if target not in grouped_data:
            grouped_data[target] = []
        grouped_data[target].append(d)
    return grouped_data


def generate_md_string(target: str, runs: list[dict]) -> str:
    result = f'## {target} trace\n'
    result += '### Legend\n'
    result += (
        '`[run order:hop order]`\n'
        "E.g: 1:4 means that you are looking at the 1st run's 4th hop.\n\n"
    )
    run_dates = [f'{i+1}: {d["date"]}' for i, d in enumerate(runs)]
    result += '**Run Dates**\n- '
    result += ('\n- '.join(run_dates)) + '\n'
    result += '### Graph\n'
    result += '```mermaid\ngraph\n'
    for i, run in enumerate(runs):
        hops = run['hops']
        for j in range(len(hops) - 1):
            curr_hop = hops[j]
            next_hop = hops[j + 1]
            result += f'{curr_hop["domain"]} --> |{i + 1}:{curr_hop["hop"]}| {next_hop["domain"]}\n'
    result += '```\n'
    return result


project_source = 'https://github.com/peter-gy/trace-vis'
# avoid hairball graphs
max_runs_per_graph = 7

if __name__ == '__main__':
    data: typing.Iterator[dict] = itertools.chain.from_iterable(json.loads(open(data_path).read()))
    grouped_data = grouped_data_by_target(data)

    for target, runs in grouped_data.items():
        loguru.logger.info(f'Generating markdown fragment for {target}')
        # Avoid hairball graphs
        used_runs = runs if len(runs) <= max_runs_per_graph else runs[::int(len(runs) / max_runs_per_graph)]
        loguru.logger.debug(f'Using {len(used_runs)} runs out of the recorded {len(runs)} runs')
        md_string = generate_md_string(target, used_runs)
        with open(f'md/{target}.md', 'w') as f:
            f.write(md_string)

    loguru.logger.info('Generating index.md')
    with open(f'md/index.md', 'w') as f:
        f.write('# Traces\n')
        f.write(f'[Source Code]({project_source})\n')
        f.write('\n'.join(f'@import "./{target}.md"' for target in grouped_data.keys()))
