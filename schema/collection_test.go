package schema

import (
	"fmt"
	"testing"
)

func TestCollectionSchema(t *testing.T) {
	cases := []schemaTestCase{
		{
			name:       "Valid collection with required fields",
			schemaPath: "./collection.json",
			jsonPath:   "./test-fixtures/collection-minimum-required.json",
		},
		{
			name:       "Valid collection with links",
			schemaPath: "./collection.json",
			jsonPath:   "./test-fixtures/collection-with-non-empty-links.json",
		},
		{
			name:       "Valid collection with empty links",
			schemaPath: "./collection.json",
			jsonPath:   "./test-fixtures/collection-with-empty-links.json",
		},
		{
			name:             "Invalid collection with null links",
			schemaPath:       "./collection.json",
			jsonPath:         "./test-fixtures/collection-with-null-links.json",
			goldenResultPath: "./golden-results/invalid-collection-with-null-links.txt",
		},
		{
			name:             "Invalid collection with non-url links",
			schemaPath:       "./collection.json",
			jsonPath:         "./test-fixtures/collection-with-non-url-links.json",
			goldenResultPath: "./golden-results/invalid-collection-with-non-url-links.txt",
		},
	}

	for _, testCase := range cases {
		t.Run(fmt.Sprintf("%s %s", t.Name(), testCase.name), func(t *testing.T) {
			verifySchema(t, testCase)
		})
	}
}
