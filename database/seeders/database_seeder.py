from . import user_seeder as UserSeeder


class DatabaseSeeder:
    """
    A class responsible for running database seeders.

    This class aggregates and manages the execution of individual seeders,
    such as the UserSeeder, to populate the database with initial data.
    """

    def run(self):
        """
        Executes the run method of each individual seeder.

        This method calls the run method of the UserSeeder class, which
        is responsible for seeding user data into the database. Additional
        seeders can be added and executed in this method as needed.
        """
        UserSeeder.run()


if __name__ == "__main__":
    db = DatabaseSeeder()
    db.run()
