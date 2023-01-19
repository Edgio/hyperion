package schema

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"testing"

	"github.com/hexops/gotextdiff"
	"github.com/hexops/gotextdiff/myers"
	"github.com/hexops/gotextdiff/span"
	"github.com/xeipuuv/gojsonschema"
)

// schemaTestCase represents a single test case to validate
// a schema against a given json file. Validation on the test
// cases may expect to fail (negative test cases).
type schemaTestCase struct {
	// Name of the test case. Gets printed as part of the test run.
	name,
	// Path to the JSON Schema file
	schemaPath,
	// Path to the JSON file to validate
	jsonPath,
	// Path to the golden result to compare against. A zero
	// value for this path means that the test case should not
	// produce should be a positive test case (produces no validation errors).
	goldenResultPath string
}

// verifySchema validates a JSON Schema located at "schemaPath"
// against JSON located at "jsonPath". It should match the results
// located at "goldenResult"
func verifySchema(t *testing.T, testCase schemaTestCase) {
	expectValid := len(testCase.goldenResultPath) == 0
	schemaFileUrl := toAbsolutePath(testCase.schemaPath)
	documentFileUrl := toAbsolutePath(testCase.jsonPath)
	schemaLoader := gojsonschema.NewReferenceLoader(fmt.Sprintf("file://%s", schemaFileUrl))
	documentLoader := gojsonschema.NewReferenceLoader(fmt.Sprintf("file://%s", documentFileUrl))

	// validate json
	result, err := gojsonschema.Validate(schemaLoader, documentLoader)

	if err != nil {
		panic(err)
	}

	// concatenate all the errs together to form the actual result
	validationErrors := result.Errors()
	sortedErrors := make([]string, len(validationErrors))

	for i, e := range validationErrors {
		sortedErrors[i] = fmt.Sprintf("[%s] %s\n", e.Field(), e.Description())
	}

	sort.Strings(sortedErrors)

	actual := strings.Join(sortedErrors, "")

	if *update && !expectValid {
		t.Logf("Writing golden result. Please review before committing: %s\n", testCase.goldenResultPath)
		if err := ioutil.WriteFile(testCase.goldenResultPath, []byte(actual), 0644); err != nil {
			panic(err)
		}
		return
	}

	var expected []byte

	if actual == "" && testCase.goldenResultPath != "" {
		t.Fatalf("JSON document %s validated but a goldenResultPath was given. Expected goldenResultPath to be empty.", testCase.jsonPath)
	}

	if !expectValid {
		if expected, err = ioutil.ReadFile(testCase.goldenResultPath); err != nil {
			panic(err)
		}
	}

	// check if the actual is the same as the expected
	if !bytes.Equal([]byte(actual), expected) {
		edits := myers.ComputeEdits(span.URIFromPath(testCase.goldenResultPath), string(expected), actual)
		diff := fmt.Sprint(gotextdiff.ToUnified(testCase.goldenResultPath, t.Name(), string(expected), edits))
		t.Fatalf("Expectations not met:\n%s", diff)
	}
}

// toAbsolutePath returns an absolute path of the relative path given to it.
// The returned path is based on the current
// working directory derived from os.Getwd()
func toAbsolutePath(relativePath string) string {
	workingDir, err := os.Getwd()
	log.Println(workingDir)

	if err != nil {
		panic(err)
	}

	absolutePath := filepath.Clean(filepath.Join(workingDir, relativePath))

	// This converts the path to be compatible with URL schemes.
	// Mainly useful on Windows machines to deal with their backwards slashes
	// This pretty inert on *nix
	return filepath.ToSlash(absolutePath)
}

func Test_ToAbsolutePath(t *testing.T) {
	filePath := toAbsolutePath("./collection.json")

	if !strings.HasSuffix(filePath, "/schema/collection.json") {
		t.Fatalf("toAbsolutePath did not return the expected file path. Actual: %s", filePath)
	}
}
