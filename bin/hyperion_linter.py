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



class hyperion_finding:

    TYPE_ERROR=1
    TYPE_WARNING=2

    def __init__(self, a_section, a_path,
                 a_msg, a_type = TYPE_ERROR):
        self.type = a_type
        self.section = a_section
        self.path = a_path
        self.msg = a_msg


class hyperion_linter:


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
        #verbose("Spec:")
        #verbose(self.spec)

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
            print("%s Section: %s   Path: %s:  %s" % ("WARN" if error.type == hyperion_finding.TYPE_WARNING else "ERR", error.section, error.path, error.msg))


    # /// \brief   Lint how paths are specified
    # /// \details
    # /// \return  List of hyperion_error objects identified or None
    def lint_paths(self):
        retval = []
        if ("servers" not in self.spec or
            len(self.spec["servers"]) == 0 or
            "url" not in self.spec["servers"][0]):
            # definitely failed
            retval.append(hyperion_finding("paths", 0, "servers[0].url doesn't exist"))
        else:
            url = self.spec["servers"][0]["url"]

            # must be relative
            if url.startswith("/"):
                retval.append(hyperion_finding("paths", "servers[0].url", "starts with '/', but must be a relative path"))

            # must use - for words in path
            if "_" in url:
                retval.append(hyperion_finding("paths", "servers[0].url", "uses '_' as a separator.  Must use '-'"))

            # should lowercase chars
            if not url.islower():
                retval.append(hyperion_finding("paths", "servers[0].url", "uses uppercase chars" % url, hyperion_finding.TYPE_WARNING))

        for path_id in self.spec["paths"]:
            path_val = self.spec["paths"][path_id]
            verbose("Analyzing path: '%s' -> '%s'" % (path_id, path_val))

            # must use - for words in path
            if "_" in path_id:
                retval.append(hyperion_finding("paths", "path.%s" % path_id, "uses '_' as a separator.  Must use '-'"))

            # must use snake_case for qs

            # should lowecase chars
            if not path_id.islower():
                retval.append(hyperion_finding("paths", "paths.%s" % path_id, "uses uppercase chars", hyperion_finding.TYPE_WARNING))
        return retval

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
        allowed_status_codes = [200, 201, 202, 204,

                                301, 303, 304, 307, 308,

                                400, 401, 403, 404, 405,
                                409, 413, 422, 429,

                                500, 502, 503, 504]
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
