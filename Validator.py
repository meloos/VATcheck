class Validator(object):

    def isNumber(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate(self, value):
        if value == "":
            return False

        if len(value) != 10:
            return False

        if not self.isNumber(value):
            return False

        checksum = 6 * int(value[0]) + 5 * int(value[1]) + 7 * int(value[2]) + 2 * int(value[3]) + 3 * int(value[4]) + 4 * int(value[5]) + 5 * int(value[6]) + 6 * int(value[7]) + 7 * int(value[8])
        checksum = checksum % 11

        if int(value[9]) != checksum:
            return False

        return True
