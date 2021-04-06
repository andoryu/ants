from enum import Enum, auto

from AntTrail.AntBase import Action
from AntTrail.AntMap import AntMap


class AntRunner:
    def __init__(self):
        self.ant_map = AntMap()
        self.ant_nest = None
        self.step_limit = 0
        self.trail_len = 0

        self.trail_ratio_reduction = False
        self.trail_ratio_dec = False

    def load_map(self, map_definition_file):
        self.ant_map.load_definition(map_definition_file)
        self.ant_map.raw_print()
        self.trail_len = self.ant_map.trail_len
        print("Trail length: {}".format(self.trail_len))
        #self.ant_map.pretty_print()

    def set_step_limit(self, step_limit):
        self.step_limit = step_limit

    def set_ant_nest(self, ant_nest):
        self.ant_nest = ant_nest.AntNest()

    def run(self):
        epoch = 1
        successfull_ants = []

        while True:
            ants = self.ant_nest.get_ant_list()
            ant_results = []


            if self.trail_ratio_reduction:
                self.trail_ratio_dec = False

            for ant in ants:
                #print("Epoch {}, ant {}".format(epoch, ant.id))

                self.ant_map.reset()
                result = self.run_ant(ant)
                #add some data
                result["id"] = ant.id
                #print(result)
                ant_results.append(result)

            successfull_ants = successfull_ants + [self.ant_nest.ants[res['id']] for res in ant_results if res['finished']]

            # if in trail reduction mode and the path steps aren't shrinking - exit
            if self.trail_ratio_reduction:
                if not self.trail_ratio_dec:
                    self.epoch_count = self.epoch_count + 1

                if self.epoch_count ==  20:
                    print("Finishing - 20 epochs with no step improvement")

                    #run the successfull ants with full logging.
                    for ant in successfull_ants:
                        print("Ant: Epoch {}, ID {}".format(ant.epoch, ant.id))
                        #print(ant.export())
                        #self.run_ant(ant, log=True)
                    break


            epoch = epoch + 1
            self.ant_nest.epoch(epoch, ant_results)



    def run_ant(self, ant, log=False):
        steps = 0
        pos = 0
        finished = False

        self.ant_map.reset()
        view = self.ant_map.get_ant_view()

        if log:
            print(ant)

        #TODO:  add code to track unique pheremone squares visited as a
        #       performance metric
        while True:

            if log:
                print("Step: {} - ".format(steps), end="")
                print("location:  {}".format(self.ant_map.ant_location))

            if steps >= self.step_limit:
                break

            if pos >= self.trail_len-1 and not self.trail_ratio_reduction:
                print("Entering trail step reduction window")
                print(" - Current steps to complete path {}".format(steps))
                self.trail_ratio_reduction = True
                self.trail_steps = steps
                self.epoch_count = 1

            if pos >= self.trail_len-1:
                break

            action = ant.next(view)

            if log:
                print("  ", view, action)

            if action == Action.ADVANCE:
                result = self.ant_map.ant_advance()
            if action == Action.ROT_CCW:
                result = self.ant_map.ant_rotate_ccw()
            if action == Action.ROT_CW:
                result = self.ant_map.ant_rotate_cw()

            view = result["view"]
            pos = result["pos"]
            finished = (pos == self.trail_len-1)

            if log:
                print("  pos: ", pos)

            steps = steps + 1

        #check if we have improved the steps to finish
        if self.trail_ratio_reduction:
            if steps<self.trail_steps:
                print(" - New steps to complete path {}".format(steps))
                self.trail_steps = steps
                self.trail_ratio_dec = True


        #return some results
        return {
            "steps": steps,
            "trail progress": pos,
            "finished": finished
        }
