# Hybrid Nutrition Virtual Assitant

We wanted to make nutrition easy to track for everyone, so we thought
we would upgrade Alexa's ability to answer nutrition related questions.

Alexa skills are just voice-to-text in front of an AWS lambda function,
so this function gets a nutrition sentance (or utterance in alexa parlance)
sends it to a knowledge extraction model trained on food information (edamam)
and returns the result to the speaker.

The goal is to make tracking macros with Hybrid Nutrition, or any nutrition service,
easier with the speach technology powered by Alexa. 

If you're not familiar with the alexa voice model or lambda functions,
check out the references below.

## Dependencies
- Amazon Alexa
- Edamam Nutrition Analysis API

## Installation
- We encorague forks
- install vs code Alexa VS code extension to test changes alexa voice model
in the simulator.
- Create a developer account on edamam.com to get API keys.

## Testing
- Commit changes to master and deploy your own development version of the skill from the alex skill plugin, or simply pushing to your own alexa master.

## Contributing
Interested in a feature? create an issue and and let us know features you would like to see.  
Want to build a feature? Pull requests are welcome.

## References
[Alexa Documentation](https://developer.amazon.com/en-US/docs/alexa/custom-skills/steps-to-build-a-custom-skill.html)  
[Edamam Food API](https://developer.edamam.com/)