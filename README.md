# Hybrid Nutrition Virtual Assitant


Staying on track with nutrition should be as simple as asking a question, so we decided to upgrade Amazon Alexa's ability to answer nutrition related questions.

Alexa skills are just voice-to-text in front of an AWS lambda function,
so this function gets a nutrition sentance (or utterance in alexa parlance)
sends it to a knowledge extraction model trained on food information (edamam)
and returns the result to the speaker.

The goal is to make tracking macros with Hybrid Nutrition, or any nutrition service,
easier with the speach technology powered by Alexa. 

If you're not familiar with the alexa voice model or lambda functions, check out the references below.

## Dependencies
- Amazon Alexa
- Edamam Nutrition Analysis API

## Installation
- We encorague forks
- The Preferred method of Testing and Development is via the Alexa VScode extension. 
- Create a developer account on edamam.com to get free API keys for the Nutrition Analysis API.

## Testing
- Commit changes to master and deploy your own development version of the skill from the alex skill plugin, or simply pushing to your own alexa master.

## Contributing
Interested in a feature? create an issue and and let us know features you would like to see.  
Want to build a feature? Pull requests are welcome. Submit your pull request along with Alexa simulator results. 

## References
[Alexa Documentation](https://developer.amazon.com/en-US/docs/alexa/custom-skills/steps-to-build-a-custom-skill.html)  
[Edamam Food API](https://developer.edamam.com/)
