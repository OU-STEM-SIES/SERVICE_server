# SERVICE

## API reference

You can use any HTTP API testing tool for the API, such as the powerful and free (for basic use) [Postman](https://www.postman.com). Of course you can simply use ```curl```, but this gets unwieldy for longer data submissions

If you have access to a Mac, I strongly recommend [Paw](https://paw.cloud), which is similar in purpose, but with a kinder UI, and some additional environment switching capabilities.

There is a pack of API test calls already configured for Paw in the SETUP directory under the filename

`API test (Paw document).paw`.

You will only need to change the environment variables which indicate the server and account to use, as the API should be unchanged. It may also be possible to import this file into other API-testing utilities.

All API calls are in the form of HTTPS GET or POST requests, with additional parameters in the URL, header and/or body of the request as detailed below.

- <a href="#RequestAuthorisationToken">Request authorisation token</a>
- <a href="#LogoutAndDeAuthorise">Logout and de-authorise</a>
- <a href="#GetCurrentUser">Get current user</a>
- <a href="#GetUsersProfile">Get user's profile</a>
- <a href="#GetCirclesOfSupport">Get Circles of Support</a>
- <a href="#GetUserLog">Get user log</a>
- <a href="#GetMoodsByDatetimes">Get moods by datetimes</a>
- <a href="#GetMoodsByPage">Get moods by page</a>
- <a href="#AddMood">Add mood</a>
- <a href="#AddWellbeingAndActivities">Add wellbeing and activities</a>
- <a href="#AddSupporter">Add supporter</a>
- <a href="#EditMoveSupporter">Edit/Move supporter</a>
- <a href="#RemoveDeleteSupporter">Remove/Delete supporter</a>

<!--

---
### Name
Description and function

###### HTTP GET URL
`URL`
###### HTTP GET URL parameters
`URL Parameters`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### HTTP POST BODY parameters
`BODY Parameters`
###### Typical response
```json
[Example response]
```
-->

---
<a name="RequestAuthorisationToken"></a>
### Request authorisation token
Rather than perform the computationally intense task of encrypting a password with every API call, the API will generate a unique token value for the account, and that value can be used instead of the username and password. Since the API calls should all take place via HTTPS, the details remain private. The token can be regenerated as needed, although the API user will then need to re-authenticate via this API call to get the new token.

The response contains the user's basic data, plus an authentication token which can be included in the header of all subsequent API calls.

###### HTTP GET URL
`https://your.server.address:443/api-auth/`
###### BODY parameters
`username=yourusername&password=yourpassword` (replace *yourusername* and *yourpassword* as appropriate)
###### Typical response
```json
{
  "token": "f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07",
  "id": 7,
  "username": "Neo",
  "first_name": "Thomas",
  "last_name": "Anderson",
  "email": "Neo@whatisthematrix.org",
  "last_login": null
}
```

---
<a name="LogoutAndDeauthorise"></a>
### Logout and de-authorise
This terminates the user's session, and also deletes the stored authorisation token, meaning that in order to do anything else in this system, the user or app will have to re-authenticate with the username and password (which will generate a new authorisation key) using the `Request authorisation token` call documented above.

###### HTTP GET URL
`https://your.server.address:443/logoutapi/`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
{
  "response": "Successfully logged out."
}
```

---
<a name="GetCurrentUser"></a>
### Get current user
This returns basic user information, similar to the `Request authorisation token` call, except that it does not return the authorisation token. It's mostly redundant, since you get all these details at login anyway, and basically is just test that the authorisation tokens work.

###### HTTP GET URL
`https://your.server.address:443/api/users/`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
{
	"id": 7,
	"username": "Neo",
	"first_name": "Thomas",
	"last_name": "Anderson",
	"email": "Neo@whatisthematrix.org",
	"last_login": null
	}
```

---
<a name="GetUsersProfile"></a>
### Get user's profile
Returns the full user profile details of the current user, or, if suitably authorised, a specified user. The user profile is a secondary database record, separate from the basic user identification and authorisation record, and it contains supplementary and demographic information about the user. Most fields in the profile are optional (at the moment). For a breakdown of the fields and accepted range of values, see the source code in `user_profile/models.py`.

###### HTTP GET URL
`https://your.server.address:443/api/profile/`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
[
	{
		"id": 7,
		"user": {
			"id": 7,
			"username": "Neo",
			"first_name": "Thomas",
			"last_name": "Anderson",
			"email": "Neo@whatisthematrix.org",
			"last_login": null
			},
		"role": "SUP",
		"phone": "phone1",
		"image": "http://your.server.address:443/media/1.jpg",
		"date_of_birth": "1990-01-14",
		"gender": "MALE",
		"ethnicity": "MXED",
		"education": "DEGR",
		"disability": "NONE",
		"marital_status": "SING",
		"smoking": false,
		"alcohol_units_per_week": 7,
		"health_conditions": [
			"0"
			],
		"things_liked": "",
		"things_disliked": "",
		"family_has": false,
		"family_bond": null,
		"community_bond": null,
		"social_groups": null,
		"social_group_other": null,
		"social_bond": null,
		"link_worker_has": false,
		"link_worker_bond": null
		}
	]
```

---
<a name="GetCirclesOfSupport"></a>
### Get Circles of Support
Each Person-At-Centre has three (notionally concentric) Circles of Support - basically three separate lists of social contacts, of differing closeness. This call returns the user's profile, plus three lists of `supporter` objects. `Supporter` objects are a superset of user profiles which supplement the user_profile object with a couple of additional fields relevant to their supporting role relative to the  PAC they support.

###### HTTP GET URL
`https://your.server.address:443/api/cos/`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
[
	{
		"user_profile": {
			"id": 7,
			"user": {
				"id": 7,
				"username": "jalay_pac",
				"first_name": "Jef",
				"last_name": "Lay",
				"email": "Jef.Lay@open.ac.uk",
				"last_login": null
				},
			"role": "SUP",
			"phone": "phone1",
			"image": "http://127.0.0.1:8000/media/1.jpg",
			"date_of_birth": "2021-12-07",
			"gender": "PNTD",
			"ethnicity": "MXED",
			"education": "DEGR",
			"disability": "NONE",
			"marital_status": "SING",
			"smoking": false,
			"alcohol_units_per_week": 7,
			"health_conditions": [
				"0"
				],
			"things_liked": "",
			"things_disliked": "",
			"family_has": false,
			"family_bond": null,
			"community_bond": null,
			"social_groups": null,
			"social_group_other": null,
			"social_bond": null,
			"link_worker_has": false,
			"link_worker_bond": null
			},
		"circle_of_support_1": [],
		"circle_of_support_2": [],
		"circle_of_support_3": [
			{
				"id": 1,
				"user_profile": {
					"id": 14,
					"user": {
						"id": 21,
						"username": "Thomas_Anderson_20211209_104854_095553",
						"first_name": "Thomas",
						"last_name": "Anderson",
						"email": "theone_optional@example.com",
						"last_login": null
						},
					"role": "SUP",
					"phone": null,
					"image": "http://127.0.0.1:8000/media/1.jpg",
					"date_of_birth": "2021-12-09",
					"gender": "PTSD",
					"ethnicity": "OTHR",
					"education": "NONE",
					"disability": "NONE",
					"marital_status": "SING",
					"smoking": false,
					"alcohol_units_per_week": 0,
					"health_conditions": [
						"0"
						],
					"things_liked": "",
					"things_disliked": "",
					"family_has": false,
					"family_bond": null,
					"community_bond": null,
					"social_groups": null,
					"social_group_other": null,
					"social_bond": null,
					"link_worker_has": false,
					"link_worker_bond": null
					},
				"group": "OTHR",
				"how_often_expected_interaction": 1
				}
			]
		}
	]
```

---
<a name="GetUserLog"></a>
### Get user log
Whenever a user makes a change to their profile, their password, or their circles of support, a log entry is created with a timestamp, plus a JSON representation of the data before and after the change (except for passwords, which aren't logged in any human-readable format).

###### HTTP GET URL
`https://your.server.address:443/api/log/`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
[
	{
		"id": 1,
		"timestamp": "2021-12-09T10:48:54.121866Z",
		"user": 7,
		"type": "COFU",
		"description": "User 7 (Thomas Anderson) registered a new Supporter: Carrie-Ann Moss to their circle 1.",
		"prediffjson": null,
		"postdiffjson": {
			"id": 1,
			"user_profile": {
				"id": 14,
				"user": {
					"id": 21,
					"username": "Trinity",
					"first_name": "Carrie-Ann",
					"last_name": "Moss",
					"email": "trinity@whatisthematrix.org",
					"last_login": null
				},
				"role": "SUP",
				"phone": null,
				"image": "/media/1.jpg",
				"date_of_birth": "1984-12-09",
				"gender": "PTSD",
				"ethnicity": "OTHR",
				"education": "NONE",
				"disability": "NONE",
				"marital_status": "MARR",
				"smoking": false,
				"alcohol_units_per_week": 0,
				"health_conditions": [
					"0"
					],
				"things_liked": "",
				"things_disliked": "",
				"family_has": false,
				"family_bond": null,
				"community_bond": null,
				"social_groups": null,
				"social_group_other": null,
				"social_bond": null,
				"link_worker_has": false,
				"link_worker_bond": null
				},
			"group": "OTHR",
			"how_often_expected_interaction": 1
			}
		}
	]
```

---
<a name="GetMoodsByDatetimes"></a>
### Get moods by datetimes
Returns a list of mood objects for the current user (or specified user if called by someone with elevated permissions). The returned list is dictated by a start and end datetime, or by a start datetime and a maximum count.

###### HTTP GET URL
`https://your.server.address:443/api/moods/`
###### HTTP GET URL parameters
`id`: The user id (optional, defaults to current user).  
`limit`: integer. The maximum number of records to return.  
`fromdt`: Datetime from which moods should be returned.  
`todt`: Datetime to which moods should be returned.  

Datetime expected format is Javascript URI-encoded, e.g.:
```javascript
encodeURIComponent("2015-02-04T05:10:58+05:30");
```
which results in `2015-02-04T05%3A10%3A58%2B05%3A30`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
[
	{
		"id": 84,
		"user": 5,
		"current_mood": "RX",
		"time": "2021-11-12T00:35:21.959368Z",
		"include_wellbeing": true,
		"wellbeing": 4,
		"previouswellbeing": null,
		"loneliness": 3,
		"previousloneliness": null,
		"pastimes": [
			{
				"whatdoing": "COOK",
				"whowith": [
					20,
					45,
					48
					]
				}
			],
		"spoketosomeone": false,
		"spoketosomeone_who": "Ashla Bluett",
		"hours_bed": 2,
		"hours_sofa": 1,
		"hours_kitchen": 2,
		"hours_garden": 1
		},
	{
		"id": 1409,
		"user": 5,
		"current_mood": "BD",
		"time": "2021-11-11T18:15:00.123456Z",
		"include_wellbeing": true,
		"wellbeing": 7,
		"previouswellbeing": 0,
		"loneliness": 7,
		"previousloneliness": 6,
		"pastimes": [
			{
				"whatdoing": "GARD",
				"whowith": [
					91
					]
				},
			{
				"whatdoing": "MUS",
				"whowith": []
				}
			],
		"spoketosomeone": true,
		"spoketosomeone_who": "Dad",
		"hours_bed": 1,
		"hours_sofa": 2,
		"hours_kitchen": 3,
		"hours_garden": 4
	},
	{
		"id": 1408,
		"user": 5,
		"current_mood": "SD",
		"time": "2021-11-11T18:10:58Z",
		"include_wellbeing": false,
		"wellbeing": 0,
		"previouswellbeing": 0,
		"loneliness": 0,
		"previousloneliness": 6,
		"pastimes": [],
		"spoketosomeone": false,
		"spoketosomeone_who": "",
		"hours_bed": 0,
		"hours_sofa": 0,
		"hours_kitchen": 0,
		"hours_garden": 0
		},
	{
		"id": 83,
		"user": 5,
		"current_mood": "CL",
		"time": "2021-11-11T12:35:21.959368Z",
		"include_wellbeing": false,
		"wellbeing": null,
		"previouswellbeing": null,
		"loneliness": null,
		"previousloneliness": null,
		"pastimes": [],
		"spoketosomeone": false,
		"spoketosomeone_who": null,
		"hours_bed": null,
		"hours_sofa": null,
		"hours_kitchen": null,
		"hours_garden": null
		}
	]
```

---
<a name="GetMoodsByPage"></a>
### Get moods by page
Much like the previous call, this returns a list of moods. However, rather than using datetime delimiters, this call returns moods page by page, starting with the most recent, where a page has a specified length. So if the page length is 5, the first page would return the most recent mood and the previous 4. The second page would return 6-10, the third 11-15, and so on until there are no more moods.

###### HTTP GET URL
`https://your.server.address:443/api/pagedmoods/`
###### HTTP GET URL parameters
`id`: The user id (optional, defaults to current user).  
`start`: integer. The page number to return.  
`howmanymoods`: integer. The number of moods per page.  
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical response
```json
{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 2,
			"user": 7,
			"current_mood": "DEPR",
			"time": "2021-11-11T18:15:00.123456Z",
			"include_wellbeing": true,
			"wellbeing": 7,
			"previouswellbeing": null,
			"loneliness": 7,
			"previousloneliness": null,
			"pastimes": [
				{
					"whatdoing": "WORK",
					"whowith": [
						1
						]
					},
				{
					"whatdoing": "COMP",
					"whowith": []
					}
				],
			"spoketosomeone": true,
			"spoketosomeone_who": "Dad",
			"hours_bed": 1,
			"hours_sofa": 2,
			"hours_kitchen": 3,
			"hours_garden": 4
			},
		{
			"id": 1,
			"user": 7,
			"current_mood": "SAD",
			"time": "2021-11-11T18:10:58Z",
			"include_wellbeing": false,
			"wellbeing": 0,
			"previouswellbeing": null,
			"loneliness": 0,
			"previousloneliness": null,
			"pastimes": [],
			"spoketosomeone": false,
			"spoketosomeone_who": "",
			"hours_bed": 0,
			"hours_sofa": 0,
			"hours_kitchen": 0,
			"hours_garden": 0
			}
		]
	}
```

---
<a name="AddMood"></a>
### Add mood
Records a mood object to the database. This call accepts a short mood record containing just a timestamp and mood, whereas another accepts a longer wellbeing record containing additional information. The response contains the created mood object, including the fields not included in the POST.

###### HTTP POST URL
`https://your.server.address:443/api/moods/`
###### HTTP GET URL parameters
`URL Parameters`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### HTTP POST BODY parameters
`current_mood`: string. An abbreviated mood descriptor such as HAPP (happy), ALAR (alarmed), etc..  
`time`: A datetime timestamp for the mood.  

Datetime expected format is Javascript URI-encoded, e.g.:  

```javascript
encodeURIComponent("2015-02-04T05:10:58+05:30");
```
which results in `2015-02-04T05%3A10%3A58%2B05%3A30`
###### Typical response
```json
{
	"id": 37,
	"user": 7,
	"current_mood": "ALAR",
	"time": "2022-01-05T13:44:55Z",
	"include_wellbeing": false,
	"wellbeing": 0,
	"previouswellbeing": null,
	"loneliness": 0,
	"previousloneliness": null,
	"pastimes": [],
	"spoketosomeone": false,
	"spoketosomeone_who": "",
	"hours_bed": 0,
	"hours_sofa": 0,
	"hours_kitchen": 0,
	"hours_garden": 0
	}
```

---
<a name="AddWellbeingAndActivities"></a>
### Add wellbeing and activities
Similar to ```Add mood```, this call creates a mood object, though this time it includes several additional fields, and an embedded structure of activities, and supporters involved in each activity.

###### HTTP POST URL
`https://your.server.address:443/api/moods/`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### Typical HTTP POST BODY parameters

`current_mood`: string. An abbreviated mood descriptor such as HAPP (happy), ALAR (alarmed), etc.  
`time`: A datetime timestamp for the mood.  
`include_wellbeing`: Boolean string indicating that there's more data coming.  
`wellbeing` & `loneliness`: Integers from 1 to 7 indicating the appropriate emotional state.  
`pastimes`: a JSON list of pastime objects, each of which is composed of one abbreviated `whatdoing` string abbreviated description, and `whowith`: a JSON list of integer Supporter object IDs.  
`spoketosomeone`: A Boolean string value.  
`spoketosomeone_who`: A textual person description, not linked to a Supporter record.  
`hours_bed`, `hours_sofa`, `hours_kitchen`, `hours_garden`: Integer values in hours, 1-24, indicating the times spent in various locations.  

Datetime expected format is Javascript URI-encoded, e.g.:  

```javascript
encodeURIComponent("2015-02-04T05:10:58+05:30");
```
which results in `2015-02-04T05%3A10%3A58%2B05%3A30`

```json
{
	"current_mood": "DEPR",
	"time": "2021-11-11T18:15:00.123456Z",
	"include_wellbeing": true,
	"wellbeing": 7,
	"loneliness": 7,
	"pastimes": [
		{
			"whatdoing": "WORK",
			"whowith": [
				1
				]
			},
		{
			"whatdoing": "COMP",
			"whowith": []
			}
		],
	"spoketosomeone": true,
	"spoketosomeone_who": "Dad",
	"hours_bed": 1,
	"hours_sofa": 2,
	"hours_kitchen": 3,
	"hours_garden": 4
	}

```
###### Typical response
```json
{
	"id": 2,
	"user": 7,
	"current_mood": "DEPR",
	"time": "2021-11-11T18:15:00.123456Z",
	"include_wellbeing": true,
	"wellbeing": 7,
	"previouswellbeing": 8,
	"loneliness": 7,
	"previousloneliness": 6,
	"pastimes": [
		{
			"whatdoing": "WORK",
			"whowith": [
				1
				]
			},
		{
			"whatdoing": "COMP",
			"whowith": []
			}
		],
	"spoketosomeone": true,
	"spoketosomeone_who": "Dad",
	"hours_bed": 1,
	"hours_sofa": 2,
	"hours_kitchen": 3,
	"hours_garden": 4
	}
```

---
<a name="AddSupporter"></a>
### Add supporter
Takes the minimum fields required to define a person's records, and generates a user object, a user_profile object, and a supporter object for that person, then adds an entry for that supporter into a specified one of the current user's Circles Of Support. Other fields are generated automatically with default values. The email field is optional, but preferred, as it could in future be used to identify cases where a known supporter also takes on another role such as PAC or key worker.

Returns the Supporter object, which has the user_profile object embedded, which in turn has the user object embedded.

###### HTTP POST URL
`https://your.server.address:443/api/add_supporter`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### HTTP POST BODY parameters
`first_name` & `last_name` & (optional) `email`: Strings. These are the minimum values required to create a user record. Defaults will be used where needed, e.g. for a password (as this user isn't expected to log in). A username will be created from the first and last names. A user_profile object will be created to go along with the user object.  
`circle_of_support`: Integer, values from 1 to 3. Indicates which of the current user's circles of support this new supporter should be added to.  
'group': String. An abbreviation which indicates the social group type through which the user knows this person.  
'how_often_expected_interaction': Integer, from a list where 1 = daily, 2 = weekly, etc.. A prediction of interaction frequency.  
```json
{
	"new_supporter": {
		"first_name": "Thomas",
		"last_name": "Anderson",
		"email": "theone_optional@example.com"
		},
	"circle_of_support": 3,
	"group": "OTHR",
	"how_often_expected_interaction": 1
	}
```
###### Typical response
```json
{
	"supporter": {
		"id": 1,
		"user_profile": {
			"id": 14,
			"user": {
				"id": 21,
				"username": "Thomas_Anderson_20211209_104854_095553",
				"first_name": "Thomas",
				"last_name": "Anderson",
				"email": "theone_optional@example.com",
				"last_login": null
				},
			"role": "SUP",
			"phone": null,
			"image": "/media/1.jpg",
			"date_of_birth": "2021-12-09",
			"gender": "PTSD",
			"ethnicity": "OTHR",
			"education": "NONE",
			"disability": "NONE",
			"marital_status": "SING",
			"smoking": false,
			"alcohol_units_per_week": 0,
			"health_conditions": [
				"0"
				],
			"things_liked": "",
			"things_disliked": "",
			"family_has": false,
			"family_bond": null,
			"community_bond": null,
			"social_groups": null,
			"social_group_other": null,
			"social_bond": null,
			"link_worker_has": false,
			"link_worker_bond": null
			},
		"group": "OTHR",
		"how_often_expected_interaction": 1
		}
	}
```

---
<a name="EditMoveSupporter"></a>
### Edit/Move supporter
Two operations in one, this call can be used to update the basic details of an existing Supporter/user_profile/user object, or to move the Supporter object to a different tier in the current user's Circles Of Support.

Returns the Supporter object, which has the user_profile object embedded, which in turn has the user object embedded.

###### HTTP POST URL
`https://your.server.address:443/api/edit_supporter`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### HTTP POST BODY parameters
`supporter_record_id`: Integer. The existing Supporter object ID.  
`first_name` & `last_name` & (optional) `email`: Strings. These are the minimum values required to create a user record. Defaults will be used where needed, e.g. for a password (as this user isn't expected to log in). A username will be created from the first and last names. A user_profile object will be created to go along with the user object.  
`to_circle`: Integer, values from 1 to 3. Indicates which of the current user's circles of support this new supporter should be moved to.  
'group': String An abbreviation which indicates the social group type through which the user knows this person.  
'how_often_expected_interaction': Integer, from a list where 1 = daily, 2 = weekly, etc.. A prediction of interaction frequency.  
```json
{
	  "supporter_record_id": 99,
	  "to_circle": 3,
	  "first_name": "Freddie",
	  "last_name": "Mercury",
	  "group": "FRND",
	  "how_often_expected_interaction": 3
}
```
###### Typical response
Similar to ```Add Supporter```.

---
<a name="RemoveDeleteSupporter"></a>
### Remove/Delete Supporter
Given a Supporter object's unique ID, this will firstly anonymise the supporter record, replacing their corresponding user object's first_name, last_name, and email fields with generic 'anonymised' text. This is currently considered sufficient, as we can still examine mood reports and activities which included this person, and we can still differentiate this person from others, even though we can no longer truly identify them.

Optionally, if the 'delete_supporter' parameter is true, then the Supporter object and corresponding user_profile and user objects are all deleted permanently from the database. Due to cascading data requirements, this will also delete any activities which involved the supporter, and any wellbeing records which involved those activities or otherwise linked to the supporter. For this reason, this step should only be taken if essential, as it could unbalance and undermine the whole data collection process.

This call returns as a response the entire Supporter object, including embedded user_profile and user objects, before anonymisation. This is the last time those records will be seen without being anonymised, or in the case of deletion, the last time they'll be seen at all.

###### HTTP POST URL
`https://your.server.address:443/api/remove_supporter`
###### HTTP HEADER parameters
`Authorization: token f9d4c7e4b1a4ae36cdacd51d1d890150a58f3b07`
###### HTTP POST BODY parameters
`supporter_record_id`: Integer. The existing Supporter object ID.  
`delete_supporter`: Boolean string. If false (default), the supporter is merely anonymised.  
```json
{
	  "supporter_record_id": 7,
	  "delete_supporter": false
}
```
###### Typical response
Similar to ```Add Supporter```.

---

[Back to README.md](README.md)
