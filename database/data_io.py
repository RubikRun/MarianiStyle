from logger import Logger

from PySide2.QtCore import QDateTime, QDate, QTime

class DataIO:
    # Parses a data declaration string.
    # The string should be of format "part0;part1;part2;part3".
    # The type of each part should be specified with the types parameter.
    # It's a list/string of same length as the number of parts. Each element of the list/string is either 's', 'i', 'f', 't' or 'I'
    # meaning that the corresponding part will be parsed as a string, int, float, QDateTime or list[int].
    # The function returns a list of parsed values, one for each part.
    # If parsing of some part failed the result for that part will be None.
    def parse_declaration(decl, types, sep = ';'):
        for type in types:
            if type not in ['s', 'i', 'f', 't', 'I']:
                Logger.log_error("Invalid types given when parsing a data declaration. Declaration will be skipped.")
                return None
        if decl is None or len(decl) < 1:
            Logger.log_error("Given declaration string is empty. Declaration will be skipped.")
            return None
        parts = decl.split(sep)
        if len(parts) != len(types):
            Logger.log_error("Data declaration has different number of parts and types. Declaration will be skipped.")
            return None
        
        results = []
        for idx, part in enumerate(parts):
            type = types[idx]
            result = None
            if type == 's':
                result = part
            elif type == 'i':
                try:
                    result = int(part)
                except ValueError:
                    Logger.log_error("Part {} of a data declaration is not an integer. This part will be None.".format(idx))
            elif type == 'f':
                try:
                    result = float(part)
                except ValueError:
                    Logger.log_error("Part {} of a data declaration is not a float. This part will be None.".format(idx))
            elif type == 't':
                result = DataIO.parse_datetime(part)
            elif type == 'I':
                if part is not None and len(part) >= 1:
                    result = DataIO.parse_declaration(part, 'i' * len(part.split('_')), '_')
                else:
                    result = []
            results.append(result)
                
        return results

    # Creates a data declaration string from given parts and their types.
    # The types list/string should have the same number of elements/characters as the parts list.
    # Each element of the types list/string should be either 's', 'i', 'f', 't', 'I'
    # meaning that the corresponding part will be serialized as a string, int, float, QDateTime or list[int].
    # If some part is None, it will be written as an empty string.
    # Returns the created declaration string
    def create_declaration(parts, types, sep = ';'):
        for type in types:
            if type not in ['s', 'i', 'f', 't', 'I']:
                Logger.log_error("Invalid types given when creating a data declaration. Declaration will not be created.")
                return ""
        if len(parts) != len(types):
            Logger.log_error("Different number of parts and types given when creating a data declaration. Declaration will not be created.")
            return ""
        s = ""
        for idx, part in enumerate(parts):
            if part is None:
                s += sep
                continue
            type = types[idx]
            if type == 's':
                s += part + sep
            elif type == 'i' or type == 'f':
                s += str(part) + sep
            elif type == 't':
                s += DataIO.create_declaration([part.date().year(), part.date().month(), part.date().day(), part.time().hour(), part.time().minute()], "iiiii", '_') + sep
            elif type == 'I':
                s += DataIO.create_declaration(part, 'i' * len(part), '_') + sep
        s = s[:-1]
        return s

    # Parses a variable assignment string.
    # The string should be of format "$VARIABLE_NAME=VARIABLE_VALUE"
    # where VARIABLE_NAME should match the var_name parameter here
    # and VARIABLE_VALUE will be parsed as specified in the type parameter.
    # Type can be either 's', 'i' or 'f' for string, int or float.
    # If the variable assignment is not in the given format or the variable name doesn't match,
    # or the parsing fails, None will be returned.
    # Otherwise the parsed value will be returned.
    def parse_variable_assignment(asgn, var_name, type):
        if asgn.startswith('$' + var_name + '='):
            value_str = asgn[len('$' + var_name + '='):]
            if type == 's':
                return value_str
            elif type == 'i':
                try:
                    value = int(value_str)
                    return value
                except ValueError:
                    Logger.log_error("Value in a variable assignment is not an integer. Assignment will be skipped.")
            elif type == 'f':
                try:
                    value = float(value_str)
                    return value
                except ValueError:
                    Logger.log_error("Value in a variable assignment is not a float. Assignment will be skipped.")

    # Creates a variable assignment string of format "$VARIABLE_NAME=VARIABLE_VALUE"
    # with the given variable name and variable value.
    # The given type determines how the given variable value will be made to a string
    # Accepted types are 's', 'i' or 'f' for string, int or float.
    # Returns the variable assignment string
    def create_variable_assignment(var_name, var_value, type):
        asgn = "$" + var_name + "="
        if type == 's':
            asgn += var_value
        elif type == 'i' or type == 'f':
            asgn += str(var_value)
        else:
            Logger.log_error("Invalid type given when creating a variable assignment string. Assignment will not be created.")
            return ""
        return asgn

    # Parses a declaration string in format "year_month_day_hour_minute" into a QDateTime object.
    # Returns the QDateTime object, or None if something is invalid in the declaration string.
    def parse_datetime(decl, sep = '_'):
        parts = DataIO.parse_declaration(decl, "iiiii", sep)
        if parts[0] is None or parts[1] is None or parts[2] is None or parts[3] is None or parts[4] is None:
            Logger.log_error("Invalid QDateTime when parsing it from a declaration. It will be None")
            return None
        datetime = QDateTime(QDate(parts[0], parts[1], parts[2]), QTime(parts[3], parts[4]))
        return datetime