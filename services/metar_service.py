from metar import Metar


class MetarService:
    def parse(self, raw_message):
        if raw_message is None or raw_message.strip() == "":
            return None

        return Metar.Metar(raw_message)

    def temperature_f(self, observation):
        if observation is None or observation.temp is None:
            return None

        return observation.temp.value("F")

    def dewpoint_f(self, observation):
        if observation is None or observation.dewpt is None:
            return None

        return observation.dewpt.value("F")

    def wind_direction_degrees(self, observation):
        if observation is None or observation.wind_dir is None:
            return None

        return observation.wind_dir.value()

    def wind_direction_compass(self, observation):
        if observation is None or observation.wind_dir is None:
            return None

        return observation.wind_dir.compass()

    def wind_speed_mph(self, observation):
        if observation is None or observation.wind_speed is None:
            return None

        return observation.wind_speed.value("MPH")

    def wind_gust_mph(self, observation):
        if observation is None or observation.wind_gust is None:
            return None

        return observation.wind_gust.value("MPH")

    def visibility_miles(self, observation):
        if observation is None or observation.vis is None:
            return None

        return observation.vis.value("MI")

    def pressure_inhg(self, observation):
        if observation is None or observation.press is None:
            return None

        return observation.press.value("IN")

    def precipitation_last_hour_in(self, observation):
        if observation is None or observation.precip_1hr is None:
            return None

        return observation.precip_1hr.value("IN")