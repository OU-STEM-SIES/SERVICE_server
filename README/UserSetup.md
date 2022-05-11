# SERVICE

## User configuration

The setup script can import users for you.

You have two user setup choices in the setup menu:
```
  Import additional users from CSV files
  Generate example (fake) Linkworkers, PACs, supporters, moods, and wellbeing data
```

The Generate option should be self-explantory: it will create a complete set of realistic data in the database so that you can explore the system and see how it should look without actually having collected data from real users. The data is semi-randomly generated, but according to fixed parameters, which you can vary by editing the first few lines of the setup script, which should be self-explanatory:
```
# For fake data generation:
random_generation_seed_value = None  # Set this to an integer value to generate a fixed sequence of data for each value, or set it to None for different data every time.
fake_data_linkworker_count = 5
fake_data_pacs_per_linkworker = 5
fake_data_supporters_per_pac = 4
fake_data_mood_days_per_pac=14
```
The default settings above will generate two weeks of mood data for each PAC. There will be 5 Linkworkers, and 5 PAC clients linked to each Linkworker. Each PAC will also have 4 supporters: None in the outer circle, only one in the middle circle, and the rest in the inner circle. None of these user accounts will be able to log in, they're only for demonstration purposes.

---

The Import option will import lists of people's credentials from comma-separated-value (CSV) files. You'll find the files in
```
root/SETUP/imports/
```

There's one file for each kind of user account, but you can add as many lines to each file as you need.

1. *Superusers*  
   These users are the server controllers. They can access anything, including performing normally hidden options such as shutting down the server. But they're not part of the SERVICE experiment, and they can't use the mobile app to do anything. There must be at least one superuser account, which is why one is required during the first-time server setup.
2. *Researchers*  
   These are the academics who are performing the research. They can't change server settings, but they can see all gathered data from all other users.
3. *Linkworkers*  
   These are the people who look after the subjects of the data-gathering. They supervise, and can view the data of their own clients, but not that of other Linkworkers' clients.
4. *Persons At Centre* (PACs)  
   PACs are the focus of the data gathering; the users whose state of loneliness we're monitoring. Data they enter using the mobile app is visible only to the PAC himself/herself and the above groups, but not to other PACs. PACs are the only users who have Circles Of Support.
5. *Supporters*  
   These are the people who help PACs get through their day. Family members, friends, contacts. We don't collect data about them except to know one from another, and to identify them in a PAC's Circles Of Support.

All 5 of the import files use the same format, and begin with the same line:
```
username,first_name,last_name,email,password  # You can leave this line here
```
As that line implies, each subsequent line should contain comma-separated values matching the columns described in the first line.

Edit the files to include the details you want to import, and then run the setup script and select the appropriate import option. People will be imported one at a time, and if an error occurs, such as a username halfway down the list already existing (usernames have to be unique!) you can edit the file to remove the names already imported and correct the problematic entry, and then simply run the import again. Once the import successfully reaches the end of its import file, the menu will appear again.

## Running tests

You can skip this section if you wish, it's entirely optional.

If you want to test the functioning of the server, you first need to have some data. Either use the server with real users and mobile apps, or generate your own data, or use the random data generator in the setup file.

Unit tests are incomplete, but in development in `user_profile/tests`.

There is also a pack of API test calls in the SETUP directory under the filename `API test (Paw document).paw`. This is a suite of tests which can be run using the Mac utility [Paw](https://paw.cloud "Paw.cloud"). It may also be possible to import these into other API-testing utilities such as PostMan.

[Back to README.md](README.md)

Next: [Shell command reference](ShellReference.md)
