import unittest
import os
import base64

from loader import export_project_description_from_readme
from github import Github

class TestReadmeParser(unittest.TestCase):
    def test_description_extraction(self, owner, project_name):
        token = os.getenv('GITHUB_ACCESS_TOKEN') or 'GITHUB_ACCESS_TOKEN'

        g = Github(token)
        repo = g.get_repo(f"{owner}/{project_name}")

        base_dir = f'./projects/{project_name}'
        project_description = repo.description

        if project_description is None:
            read_me = repo.get_readme()
            project_description = export_project_description_from_readme(base64.b64decode(read_me.content))
            print("Project description from README.md", project_description)

        print(project_description)

    def test_no_description(self):
        # Test case where there's no description after the H1 heading
        content = "# Project Title\n\n## Next Section"
        self.assertIsNone(export_project_description_from_readme(content))

    def test_no_heading(self):
        # Test case where there's no H1 heading
        content = "This is some content without a heading."
        self.assertIsNone(export_project_description_from_readme(content))

    # Add more test cases as needed to cover different scenarios

if __name__ == '__main__':
    unittest.main()
