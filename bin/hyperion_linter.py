#!/usr/bin/env python3

#//////////////////////////////////////////////////////////////////////////
#//
#// Copyright EdgeCast Networks 2007-2023
#//
#// Prognosis:  Hyperion linter command/library
#// Date:       10/14/2023
#// Authors:    David Andrews
#//
#//////////////////////////////////////////////////////////////////////////

# // Includes
import sys
import os
import yaml
import argparse
import traceback

# // Variables

VERBOSE=0
LINT_SECTIONS=['all','paths','versioning','naming','status-codes','dates','time-series','keywords','document-structure']

# // Functions

# /// \brief   print a verbose message
# /// \details
# /// \return
# /// \param   a_msg The message to print
# /// \status  ALPHA
def verbose(a_msg):
    if VERBOSE == 1:
        # etc verbose output requested
        print(a_msg)



# // Classes



class hyperion_error:
    def __init__(self, a_section, a_line, a_msg):
        self.section = a_section
        self.line = a_line
        self.msg = a_msg


class hyperion_linter:

    # // Static Variables
    LC_SERVERS = {"EC": "api-int.edgecast.com", # the default server to connect to
                  "IR500": "api-int.transactcdn.com",
                  "QA": "qa-uber.edgecast.com"}


    # // Functions

    # /// \brief   ctor
    # /// \details
    # /// \return
    # /// \param   a_sections  The sections to validate
    # /// \status  ALPHA
    def __init__(self, a_sections, a_file):

        #verbose("Sections: '%s'" % a_sections)
        #verbose("File: '%s'" % a_file)

        # // Member Variables
        self.sections = a_sections
        self.file = open(a_file)
        self.spec = yaml.load(self.file, Loader=yaml.FullLoader)


    # /// \brief   Lint some shit
    # /// \details Run all configured linters, print results from all failures
    # /// \return  True on success
    # ///          False on linter failure
    def lint(self):
        errors = []
        if "all" in self.sections:
            errors.extend(self.lint_paths())
            errors.extend(self.lint_versioning())
            errors.extend(self.lint_naming())
            errors.extend(self.lint_status_codes())
            errors.extend(self.lint_dates())
            errors.extend(self.lint_time_series())
            errors.extend(self.lint_keywords())
            errors.extend(self.lint_document_structure())
        else:
            for section in self.sections:
                if section == "paths":
                    errors.extend(self.lint_paths())
                elif section == "versioning":
                    errors.extend(self.lint_versioning())
                elif section == "naming":
                    errors.extend(self.lint_naming())
                elif section == "status-codes":
                    errors.extend(self.lint_status_codes())
                elif section == "dates":
                    errors.extend(self.lint_dates())
                elif section == "time-series":
                    errors.extend(self.lint_time_series())
                elif section == "keywords":
                    errors.extend(self.lint_keywords())
                elif section == "document-structure":
                    errors.extend(self.lint_document_structure())

        #verbose("Errors: '%s'" % errors)
        for error in errors:
            print("Section: %s   Line: %d:  %s" % (error.section, error.line, error.msg))


    # /// \brief   Lint how paths are specified
    # /// \details
    # /// \return  List of hyperion_error objects identified or None
    def lint_paths(self):
        return []

    # /// \brief   Lint how versioning is implemented
    # /// \details
    # /// \return  List of hyperion_error objects identified or None
    def lint_versioning(self):
        return []

    # /// \brief   Lint how basic naming conventions are ised
    # /// \details
    # /// \return  List of hyperion_error objects identified or None
    def lint_naming(self):
        return []

    # /// \brief   Lint how HTTP status codes used
    # /// \details
    # /// \return  List of hyperion_error objects identified or None
    def lint_status_codes(self):
        return []

    # /// \brief   Lint how dates are represented
    # /// \details
    # /// \return  List of hyperion_error objects identified or []
    def lint_dates(self):
        return []

    # /// \brief   Lint how time series data is handled
    # /// \details
    # /// \return  List of hyperion_error objects identified or []
    def lint_time_series(self):
        return []

    # /// \brief   Lint how reserved hyperion keywords and their usage
    # /// \details
    # /// \return  List of hyperion_error objects identified or []
    def lint_keywords(self):
        return []

    # /// \brief   Lint how JSON objects are structured
    # /// \details
    # /// \return  List of hyperion_error objects identified or None
    def lint_document_structure(self):
        retval = []
        retval.append(hyperion_error("document-structure", 1, "test error"))
        return retval


# handle if executed as a script
if __name__ == "__main__":
    # call out to the main linter

    parser = argparse.ArgumentParser(description="Run hyperion linter over the provided openapi3 specification file",
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--section', type=str, default='all',
                        help='Only validate the specific section of the hyperion standard.',
                        choices=LINT_SECTIONS,
                        nargs='+')
    parser.add_argument('file', type=str, help='The file to parse')
    args = parser.parse_args()
    VERBOSE=args.verbose

    l_linter = hyperion_linter(args.section, args.file)
    try:
        l_linter.lint()
    except:
        traceback.print_exc(file = sys.stdout)
        sys.exit(1)
