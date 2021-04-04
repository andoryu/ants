import importlib
import json
import sys

from AntTrail import AntRunner

sys.path.append("../src")


if __name__ == "__main__":
    try:
        cfg = json.load(open("./ant-config.json"))

        ant_nest = importlib.import_module(cfg["ant-nest"])

        runner = AntRunner.AntRunner()
        runner.set_step_limit(cfg["step-limit"])
        runner.load_map(cfg["map"])
        runner.set_ant_nest(ant_nest)

        runner.run()

    except FileNotFoundError as e:
        print(e)
