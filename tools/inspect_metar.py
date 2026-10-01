from metar import Metar


RAW_MESSAGE = (
    "PHNL 012228Z 15014KT 10SM -RA "
    "FEW022 BKN038 OVC055 25/23 A2988 "
    "RMK AO2 RAB06 P0016 T02500233 $"
)


def main():
    observation = Metar.Metar(RAW_MESSAGE)

    print(observation.string())


if __name__ == "__main__":
    main()