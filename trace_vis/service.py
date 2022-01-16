import datetime
import re
import subprocess

import loguru

import trace_vis.model as model


def run_traceroute(target: str) -> model.TraceRun:
    run_date = datetime.datetime.now()
    # Set the time (in seconds) to wait for a response to a probe
    wait_time = 1
    # Set the max time-to-live (max number of hops) used in outgoing probe packets.
    max_ttl = 32
    cmd = ['traceroute',
           '-w', str(wait_time),
           '-m', str(max_ttl),
           target]
    loguru.logger.debug(f'Running command: {" ".join(cmd)}')
    traceroute_output: str = subprocess.check_output(cmd).decode()
    return __parse_traceroute_output(traceroute_output=traceroute_output, run_date=run_date, target=target)


def __parse_traceroute_output(traceroute_output: str, run_date: datetime.datetime, target: str) -> model.TraceRun:
    hops: list[model.TraceHop] = []
    last_hop_num = 1
    for line in traceroute_output.split('\n'):
        if len(line.strip()) == 0 or '*' in line:
            continue
        hop = __parse_traceroute_output_line(line=line, last_hop_num=last_hop_num)
        last_hop_num = hop.hop
        hops.append(hop)
    return model.TraceRun(hops=hops, date=run_date, target=target)


def __parse_traceroute_output_line(line: str, last_hop_num: int) -> model.TraceHop:
    assert len(line.strip()) > 0, 'Empty line'
    assert '*' not in line, 'Line contains *'
    pattern = r'^ *(?:(\d{1,2})|)  (.*) \((.*)\)  (.+?) ms.*$'
    match = re.match(pattern, line)
    try:
        hop, domain, ip, time_ms = match.groups()
        return model.TraceHop(hop=hop if hop is not None else last_hop_num,
                              domain=domain,
                              ip=ip,
                              time_ms=float(time_ms))
    except AttributeError as e:
        loguru.logger.error(f'Failed to parse line: {line} - {e}')
