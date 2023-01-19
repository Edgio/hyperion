package schema

import (
	"flag"
	"fmt"
	"testing"
)

var update = flag.Bool("update", false, "update golden files")

func TestNodeSchema(t *testing.T) {
	cases := []schemaTestCase{
		{
			name:             "Invalid without required fields",
			schemaPath:       "./node.json",
			jsonPath:         "./test-fixtures/empty-obj.json",
			goldenResultPath: "./golden-results/invalid-without-required-fields.txt",
		},
		{
			name:       "Valid with minimum required fields",
			schemaPath: "./node.json",
			jsonPath:   "./test-fixtures/node-minimum-required.json",
		},
		{
			name:       "Valid with empty @links",
			schemaPath: "./node.json",
			jsonPath:   "./test-fixtures/node-empty-links.json",
		},
		{
			name:       "Valid with @links",
			schemaPath: "./node.json",
			jsonPath:   "./test-fixtures/node-with-links.json",
		},
		{
			name:             "Invalid with empty link value",
			schemaPath:       "./node.json",
			jsonPath:         "./test-fixtures/empty-link-value.json",
			goldenResultPath: "./golden-results/invalid-with-empty-link-value.txt",
		},
		{
			name:             "Invalid link value base_path",
			schemaPath:       "./node.json",
			jsonPath:         "./test-fixtures/invalid-base-path.json",
			goldenResultPath: "./golden-results/invalid-link-value-base-path.txt",
		},
	}

	for _, testCase := range cases {
		t.Run(fmt.Sprintf("%s %s", t.Name(), testCase.name), func(t *testing.T) {
			verifySchema(t, testCase)
		})
	}
}
