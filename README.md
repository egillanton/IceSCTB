![alt text](https://www.ru.is/skin/basic9k/i/sitelogo.svg "Reykjavik University Logo")

# IceSCTB - Icelandic Sentence Completion Twitter Bot
### Natural Language Processing
#### T-725-MALV, Málvinnsla, 2018-3

---
## Project
In this project a team implemented a Twitter bot ([MLVbot](https://twitter.com/MLVbot)), generating tweets from a Probabilistic Language Model.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Setup Virtual Enviroment

Start creating a conda enviroment.

```sh
$ conda create -n myEnv python=3.6
$ conda activate myEnv
```

Now within the virtual enviroment, install the following packages:

```
(myEnv) $ pip install TwitterAPI
(myEnv) $ conda install nltk
(myEnv) $ conda install tqdm
```

### Get Data
Download the data and the models [here](https://www.dropbox.com/s/9auvg6ytr53degw/data_and_models.zip?dl=0).

Extract the .zip file into the root of the project.

Now it should be as follow:
```
IceSCTB
├── LanguageModel.py
├── Twitter.py
├── TwitterBot.py
├── data
|   └── MIM
|   |    └── ...
|   └── ISL
|        └── ...
├── models
|   ├── LanguageModel3_ISL.pkl
|   └── LanguageModel4_ISLMIM.pkl
```

## Configure Twitter API

Open Twitter.py and specify your uniqe API keys.

```python
class Twitter:
    __consumer_key = ''
    __consumer_secret = ''
    __access_token_key = ''
    __access_token_secret = ''
    __user_id_str = ''
```

## Run The bot

```sh
(myEnv) ~/IceSCTB $ python TwitterBot.py
```

## Authors
  * [Ásmundur Guðjónsson](https://github.com/asmundur) - MSc. Language Technology Student
  * [Egill Anton Hlöðversson](https://github.com/egillanton) - MSc. Language Technology Student

## License
This project is licensed under the MIT License - see the [LICENSE.md](./doc/LICENSE.md) file for details

## References
 * [NTLK](https://github.com/nltk/nltk)
 * [TwitterAPI](https://github.com/geduldig/TwitterAPI)

