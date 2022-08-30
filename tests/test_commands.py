from unittest import TestCase
from unittest.mock import patch, Mock

from commands import CreateClientsTableCommand, AddClientCommand, ImportGithubStarsCommand


class CreateClientsTableCommandTest(TestCase):
    def setUp(self):
        self.command = CreateClientsTableCommand()

    def test_execute(self):
        with patch("commands.DatabaseManager.create_table") as mocked_create_table:
            self.command.execute()
            mocked_create_table.assert_called_with(
                table_name="clients",
                columns={
                    "id": "integer primary key autoincrement",
                    "client_name": "text not null",
                    "proiect": "text not null",
                    "informatii": "text",
                    "url":"text not null",
                    "date_added": "text not null",
                }
            )


class AddClientCommandTest(TestCase):
    def setUp(self):
        self.command = AddClientCommand()

    def test_execute(self):
        with patch("commands.DatabaseManager.add") as mocked_add_client:
            data = {
                "client_name": "mock_title",
                "proiect":"mock_proiect",
                "informatii":"mock_informatii",
                "url": "mock_url",
                "notes": "mock_notes"
            }
            result = self.command.execute(data)
            mocked_add_client.assert_called_with(
                table_name="clients",
                data=data
            )
            
            self.assertEqual(result, "Client added!")


