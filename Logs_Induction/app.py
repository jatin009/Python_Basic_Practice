import sys
import os
import enum

file_path = sys.argv[1]

if not os.path.isdir(file_path):
    print(f"File path {file_path} does not exist. Exiting...")
    sys.exit()

cpp_class = input("Enter class name: ")
cpp_file_path = file_path+"/"+cpp_class+".cpp"
cpp_class_methods = cpp_class+'::'

CPP_SINGLE_LINE_COMMENT = '//'
CPP_MULTI_LINE_COMMENT_BEGIN = '/*'
CPP_MULTI_LINE_COMMENT_END = '*/'
braces_stack = []
in_multi_line_comment = False


class FunctionStatus(enum.Enum):
    OPENED = 1,
    BODY = 2,
    NONE = 3


def find_all_occurrences_of(needle, haystack):
    location = -1
    occurrences_list = []

    while True:
        location = haystack.find(needle, location + 1)

        if location == -1:
            break
        else:
            occurrences_list.append(location)

    return occurrences_list


logged_file = open(cpp_file_path+"_new", 'w')

with open(cpp_file_path, 'r') as orig_file:

    func_status = FunctionStatus.NONE
    for line in orig_file:

        commented_line = code_line = ""
        single_line_comment_pos = line.find(CPP_SINGLE_LINE_COMMENT)
        multi_line_comment_begin_pos = line.find(CPP_MULTI_LINE_COMMENT_BEGIN)
        multi_line_comment_end_pos = line.find(CPP_MULTI_LINE_COMMENT_END)

        if in_multi_line_comment:
            # just print the line and continue

            if multi_line_comment_end_pos != -1:
                commented_line = line[:multi_line_comment_end_pos]
                code_line = line[multi_line_comment_end_pos+2:]
                in_multi_line_comment = False
            else:
                logged_file.write(line)
                continue

        if single_line_comment_pos != -1 or \
                (multi_line_comment_begin_pos != -1 and single_line_comment_pos < multi_line_comment_begin_pos):
            """
            It's just a // comment or // followed by /*, then // comment is the prioritised one
            """
            commented_line = line[single_line_comment_pos:]
            code_line = line[:single_line_comment_pos]

        elif (multi_line_comment_begin_pos != -1 and multi_line_comment_end_pos == -1) or \
                (single_line_comment_pos != -1 and multi_line_comment_begin_pos < single_line_comment_pos):
            """
            It's just a /* comment (and */ is not present in the line to close the comment) 
            or /* followed by //, then /* comment is the prioritised one
            """
            in_multi_line_comment = True
            commented_line = line[multi_line_comment_begin_pos:]
            code_line = line[:multi_line_comment_begin_pos]

        elif multi_line_comment_begin_pos != -1 and multi_line_comment_end_pos != -1 and \
                multi_line_comment_end_pos > multi_line_comment_begin_pos:
            """
            It's just a /* comment followed by */ 
            TODO: This may break if a line contains multiple pairs of /*--*/ as 
            currently it checks only for one such pair
            """
            in_multi_line_comment = False
            commented_line = line[multi_line_comment_begin_pos:multi_line_comment_end_pos+1]
            code_line = line[:multi_line_comment_begin_pos] + line[multi_line_comment_end_pos+2:]

        if code_line.find(cpp_class_methods) != -1 and len(braces_stack) == 0:
            func_status = FunctionStatus.OPENED

        opening_brace_pos = code_line.find('{')
        closing_brace_pos = code_line.find('}')

        if func_status == FunctionStatus.OPENED:

            if closing_brace_pos != -1 and opening_brace_pos != -1 and closing_brace_pos > opening_brace_pos:
                logged_file.write(line)
                func_status = FunctionStatus.NONE
                continue

            if opening_brace_pos != -1:
                logged_file.write(code_line[:opening_brace_pos+1]+'\n'+'LOG_ERROR("Entry");\n'+
                                  code_line[opening_brace_pos+1:])
                func_status = FunctionStatus.BODY
            else:
                logged_file.write(line)

        elif func_status == FunctionStatus.BODY:

            if opening_brace_pos != -1:
                logged_file.write(line)
                braces_stack.append('{')

            elif closing_brace_pos != -1:

                if len(braces_stack) > 0:
                    braces_stack.pop()
                    logged_file.write(line)
                else:
                    logged_file.write(
                        code_line[:closing_brace_pos] + '\n' + 'LOG_ERROR("Exit");\n' + code_line[closing_brace_pos:])
                    func_status = FunctionStatus.NONE

            else:
                logged_file.write(line)

        else:
            logged_file.write(line)

logged_file.close()

print(f"File {cpp_file_path+'_new'} successfully created at same location.")
