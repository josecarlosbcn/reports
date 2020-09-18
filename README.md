# Reports

This project gives you the possibility to build reports from stats in PDF format.

The reports you can get are:

* Pre-game report
* Post-game report
* Monthly report
* Accumulated Team report (include all its players)
* Accumulated Player report (only one player)

## Getting Started

Some of the libraries needed to run the application are:
* Pillow
* PyMySQL
* fpdf
* google-api-core
* google-api-python-cliente
* google-auth
* google-auth-httplib2
* google-auth-oauthlib
* matplotlib
* numpy
* pandas
* pip

### Prerequisites

You need to have this databases with data in your localhost or to have access to them
* feb_estadisticas
* fiba_stats

### Installing

You only need to download the project to your compute

## Running the tests

The directory /test has all the tests of the application

### Break down into end to end tests

* bar_char_plot_test: Let you to test a Bar Chart
* color_test: Let you to test the colors of an image
* data_monthly_test: Let you to test the functions of DataMonthly object
* data_postgame_test: Let you to test the funcions of DataPostgame object
* data_pregame_test: Let you to test the functions of Pregame object
* image_test: Let you to create an image from a file
* multibar_chart_plot_test: Let you to test a MultiBar Chart
* player_shots_test: Let you to test the functions of PlayerShots object
* season_shots_test: Let you to test the functions of SeasonShots object
* team_advanced_stats_test: Let you to test the functions of TeamAdvancedStats object
* team_shots_test: Let you to test the funcionts of TeamShots object
* test_data_accumulated: Let you to test the functions of DataAccumulated object
* test_data_player_accumulated: Let you to test the functions pf DataPlayerAccumulated object
* test_send_mail: Let you to test mail functions (send email to one or several receptors)

## Authors

* **José Carlos Liria Céspedes** - *Initial work* - josecarlosbcn@gmail.com
