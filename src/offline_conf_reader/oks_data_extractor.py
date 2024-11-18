from dataclasses import dataclass, Field, fields
from pathlib import Path
from defusedxml.ElementTree import parse


def check_for_includes(root):
    for child in root:
        if child.tag == 'include':
            return True

@dataclass
class OKSDataExtractor:
    oks_file_path: Path
    session_name:str
    buffer: object = None
    ac_couple: object = None
    pulse_dac: object = None
    pulser: object = None
    baseline: object = None
    gain: object = None
    leak: object = None
    leak_10x: object = None
    peak_time: object = None
    enable_femb_fake_data: object = None
    test_cap: object = None
    APAs: list[int] = None
    FEMBs: list[int] = None
    pulse_period: object = None
    phase_group: object = None
    phases: object = None

    def __post_init__(self):
        if self.oks_file_path == 'dummy':
            return

        tree = parse(self.oks_file_path)
        root = tree.getroot()

        if check_for_includes(root):
            raise RuntimeError('Include files are not supported, the configuration was not consolidated!')


    def get_variables(self) -> list[Field]:

        data = []
        for field in fields(self):
            if field.name == 'session_name' or field.name == 'oks_file_path':
                continue
            data += [field]

        return data
