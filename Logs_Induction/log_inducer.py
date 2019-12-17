import sys
import os
import enum

# file_path = sys.argv[1]
#
# if not os.path.isdir(file_path):
#     print(f"File path {file_path} does not exist. Exiting...")
#     sys.exit()

cpp_class = input("Enter class name: ")
cpp_file_path = "C:/Documents/VisualPractice/SnakeGameConsole_OOP/SnakeGameConsole_OOP"+"/"+cpp_class+".cpp"
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


def add_exit_log(func_body):
    end_brace_pos = func_body.rfind('}')

    if end_brace_pos != -1:
        exit_log_func_body = func_body[:end_brace_pos]+'\n' + 'LOG_ERROR("Exit");\n' + func_body[end_brace_pos:]
        return exit_log_func_body
    return func_body


logged_file = open(cpp_file_path+"_new", 'w')


with open(cpp_file_path, 'r') as orig_file:

    func_opened = False
    func_code = ""

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

        else:
            code_line = line

        if code_line.find(cpp_class_methods) != -1:  # and len(braces_stack) == 0:
            func_opened = True

        opening_brace_pos = code_line.find('{')
        closing_brace_pos = code_line.find('}')

        if func_opened:

            # if closing_brace_pos != -1 and opening_brace_pos != -1 and closing_brace_pos > opening_brace_pos:
            #     logged_file.write(line)
            #     func_status = FunctionStatus.NONE
            #     continue
            func_code = add_exit_log(func_code)
            logged_file.write(func_code)

            if opening_brace_pos != -1:
                func_code += code_line[:opening_brace_pos+1]+'\n'+'LOG_ERROR("Entry");\n' + \
                             code_line[opening_brace_pos+1:]
                # logged_file.write(code_line[:opening_brace_pos+1]+'\n'+'LOG_ERROR("Entry");\n'+
                                  # code_line[opening_brace_pos+1:])
            else:
                # logged_file.write(line)
                func_code += line

            func_opened = False
        else:
                # logged_file.write(line)
                func_code += line

logged_file.close()

print(f"File {cpp_file_path+'_new'} successfully created at same location.")
