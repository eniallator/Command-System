import async_unittest
from CommandSystem import CommandSystem

class TestCommandSystem(async_unittest.TestCase):
    
    cmd_system = CommandSystem()

    def test_add_command(self):
        self.cmd_system.add_command(
            'test',
            cmd_func=lambda arg: 'foo ' + arg,
            help_summary='sum',
            help_full='full',
            check_perms=lambda arg: True if arg == 'bar' else False
        )
        self.cmd_system.add_command(
            'other',
            cmd_func=lambda arg: 'hello ' + arg,
            help_summary=lambda arg: 'sum ' + arg,
            help_full=lambda arg: 'full ' + arg
        )

    def test_add_commandSystem(self):
        self.cmd_system.add_command_system('hello', 'hi')

    def test_get_commandSystem(self):
        self.assertTrue(isinstance(self.cmd_system.get_command_system('hello'), CommandSystem))

    def test_get_nested_commandSystem(self):
        self.cmd_system.get_command_system('hello').add_command_system('goodbye', 'bye')
        self.assertTrue(isinstance(self.cmd_system.get_command_system(['hello', 'goodbye']), CommandSystem))

    async def test_execute_valid_perms(self):
        result = await self.cmd_system.execute('test', 'bar')
        self.assertEqual(result, 'foo bar')

    async def test_execute_invalid_perms(self):
        result = await self.cmd_system.execute('test', 'foo')
        self.assertEqual(result, 'Error insufficient permissions for this command.')

    def test_get_help(self):
        result = self.cmd_system.get_help('', 'arg')
        self.assertEqual(result, 'Showing help:\n`other`: sum arg\n`hello`: hi\nTo learn more about a command, use `help <command>`')

    def test_get_help_test_full(self):
        result = self.cmd_system.get_help('test')
        self.assertEqual(result, 'full')

    def test_get_help_other_full(self):
        result = self.cmd_system.get_help('other', 'arg')
        self.assertEqual(result, 'full arg')

    def test_get_nested_help_command_system_hello(self):
        result = self.cmd_system.get_help('hello')
        self.assertEqual(result, 'Showing help for hello:\n`hello goodbye`: bye\nTo learn more about a command, use `help <command>`')

    def test_get_nested_help_command_system_goodbye(self):
        result = self.cmd_system.get_help('hello goodbye')
        self.assertEqual(result, 'Showing help for goodbye:\nTo learn more about a command, use `help <command>`')

    def test_get_help_invalid(self):
        result = self.cmd_system.get_help('error')
        self.assertEqual(result, 'Unknown command. Use "help" to get a list of commands.')


async_unittest.main()
