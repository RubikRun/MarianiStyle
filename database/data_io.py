from logger import Logger

class DataIO:
    # Parses a data declaration string.
    # The string should be of format "part0;part1;part2;part3".
    # The type of each part should be specified with the types list/string.
    # It's a list/string of same length as the number of parts. Each element of the list/string is either 's', 'i' or 'f'
    # meaning that the corresponding part will be parsed as a string, int or float.
    # The function returns a list of parsed values, one for each part.
    # If parsing of some part failed the result for that part will be None.
    def parse_declaration(decl, types):
        for type in types:
            if type not in ['s', 'i', 'f']:
                Logger.log_error("Invalid types given when parsing a data declaration. Declaration will be skipped.")
                return None
        parts = decl.split(';')
        if len(parts) != len(types):
            Logger.log_error("Data declaration has different number of parts and types. Declaration will be skipped.")
        
        results = []
        for idx, part in enumerate(parts):
            type = types[idx]
            if type == 's':
                results.append(part)
            elif type == 'i':
                try:
                    result = int(part)
                except ValueError:
                    Logger.log_error("Part {} of a data declaration is not an integer. This part will be None.")
                    result = None
                results.append(result)
            elif type == 'f':
                try:
                    result = float(part)
                except ValueError:
                    Logger.log_error("Part {} of a data declaration is not a float. This part will be None.")
                    result = None
                results.append(result)
                
        return results

    # Creates a data declaration string from given parts and their types.
    # The types list/string should have the same number of elements/characters as the parts list.
    # Each element of the types list/string should be either 's', 'i' or 'f'
    # meaning that the corresponding part will be serialized as a string, int or float.
    # If some part is None, it will be written as an empty string.
    # Returns the created declaration string
    def create_declaration(parts, types):
        for type in types:
            if type not in ['s', 'i', 'f']:
                Logger.log_error("Invalid types given when creating a data declaration. Declaration will not be created.")
                return ""
        if len(parts) != len(types):
            Logger.log_error("Different number of parts and types given when creating a data declaration. Declaration will not be created.")
            return ""
        s = ""
        for idx, part in enumerate(parts):
            if part is None:
                s += ";"
                continue
            type = types[idx]
            if type == 's':
                s += part + ';'
            elif type == 'i' or type == 'f':
                s += str(part) + ";"
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