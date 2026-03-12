
# ETEC2104 Team Git Workflow

This project uses a simplified version of the Git Flow model.

Reference:
https://nvie.com/posts/a-successful-git-branching-model/

---

# Branch Structure

master
develop
ftr/*
bug/*

---

# Branch Roles

## master

Production-ready code.

Only the instructor merges into master.

Each merge into master is tagged as a release.

Example tags:

v0.1-template
v0.2-api-working
v0.3-team-release

---

## develop

Team integration branch.

Team leads merge approved work into develop.

Develop represents the current working version of the system.

---

## ftr/*

Feature branches used for implementing new functionality.

Examples:

ftr/order-validation
ftr/tradebot
ftr/market-snapshot

---

## bug/*

Bugfix branches.

Examples:

bug/order-side-check
bug/serializer-validation

---

# Development Workflow

1. Pull latest develop

git checkout develop
git pull

2. Create feature branch

git checkout -b ftr/order-validation

3. Write code

git add .
git commit -m "added order validation"

4. Push branch

git push origin ftr/order-validation

5. Create Pull Request to develop

Team lead reviews code.

6. Merge into develop

7. Instructor reviews and merges develop → master

---

# Team Roles

Each team should assign roles:

Team Lead
- manages develop branch
- reviews pull requests

Backend Developer
- models
- serializers
- views

Client Developer
- tradebot
- API testing

QA / Debug
- endpoint testing
- validating responses
- documenting issues

---

# Key Rule

Never push directly to master.

All work must go through:

feature branch → develop → master
