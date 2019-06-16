# -*- coding: utf-8 -*-
import json
import click


class CoordinateType(click.ParamType):
    name = "coordinate"

    def convert(self, value, param, ctx):
        values = value.split(",")
        if len(values) == 2:
            lat_string, lng_string = values
            try:
                lat, lng = float(lat_string), float(lng_string)
                if -90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0:
                    return lat, lng
                self.fail(
                    f"The coordinate {value!r} are not in valid ranges:"
                    "-90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0",
                    param,
                    ctx,
                )
            except ValueError:
                self.fail(
                    f"The coordinate {value!r} are not numbers", param, ctx
                )
        else:
            self.fail(
                f"The {value!r} coordinate must have only 2 values in 'LAT,LNG' format",
                param,
                ctx,
            )


class JsonType(click.ParamType):
    name = "Dict"

    def convert(self, value, param, ctx):
        try:
            return json.loads(value)
        except json.decoder.JSONDecodeError as e:
            self.fail(f"{e}", param, ctx)


COORDINATE_TYPE = CoordinateType()
JSON_TYPE = JsonType()
