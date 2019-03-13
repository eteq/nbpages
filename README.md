# nbpages HTML cookiecutter

This is a [cookiecutter](https://github.com/audreyr/cookiecutter) template for the html flavor of nbpages.

Invoke it with:
```
cookiecutter gh:eteq/nbpages --checkout cookiecutter_html
```

## Conda Environment

The environment.yml file in the base of this repo is used by the CI to create a conda environment with all the dependencies needed to run your notebooks. Please add conda and PIP dependencies required for your notebooks to this file (you will get import/module not found errors if something needed isn't installed). This file can also be used to create a local environment to run notebooks by using:
```
conda env create -f environment.yml
conda activate notebooks_env
```

## Continuous Integration

Included are base scripts for CI implementations on Travis and CircleCI. They install conda, create a conda environment for the notebooks, and deploy to github pages (if configured). Please update/modify as needed to suite your specific needs.

## Deploying Converted Notebooks to Github Pages

The base CI scripts are configured to deploy to Github pages when job is not a pull request and is on the master branch. The Github repo must be configured for use with [Github Pages](https://help.github.com/en/articles/configuring-a-publishing-source-for-github-pages) and the publishing source must be set to gh-pages branch for this to work. Some setup is also required to configure your CI to allow this automatic deployment.

### CircleCI
1. [Generate SSH Key](https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) Note: must use modified command "ssh-keygen -m pem" on mac to generate rsa key compatible with circleCI.
2. [Add Deploy Key to Github](https://developer.github.com/v3/guides/managing-deploy-keys/) Add SSG key as a write access deploy key to the repo on github.
3. [Add SSH Key to CircleCI](https://circleci.com/docs/2.0/add-ssh-key/) Add SSH key to circleCI SSH keys config.
4. Add GH_EMAIL, GH_NAME, and BUILD_TAG environment variables to CircleCI config.yml file or to the environment variable configuration on CircleCI settings.
```
environment:
  - GH_NAME: ghname
  - GH_EMAIL: ghemail@example.com
  - BUILD_TAG: unique tag for deployment commit message
```

### TravisCI
Please see [TravisCI's](https://docs.travis-ci.com/user/deployment/pages/) detailed guide to add a personal access token to your config to enable the script to deploy to Github Pages.
