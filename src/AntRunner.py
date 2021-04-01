from enum import Enum, auto

from AntBase import Action
import AntMap


class AntRunner:
    def __init__(self, step_limit):
        self.ant_map = AntMap()
        self.step_limit = step_limit

    def configure_map(map_definition_file)
        self.ant_map.load_definition(map_definition_file)

    def run_ant(ant):
        steps = 0
        finished = False

        self.ant_map.reset()
        view = self.ant_map.get_ant_view()

        #TODO:  add code to track unique pheremone squares visited as a
        #       performance metric
        while steps < self.step_limit and not Finished:
            action = Ant.next(view)

            if action == Action.ADVANCE:
                result = self.ant_map.ant_advance()
            if action == Action.ROTCCW:
                result = self.ant_map.ant_rotate_ccw()
            if action == Action.ROTCW:
                result = self.ant_map.ant_rotate_cw()

            view = result["view"]
            finished = result["finished"]
            steps = steps + 1

        #return some results
        return {
            "steps": steps,
            "finished": finished
        }
