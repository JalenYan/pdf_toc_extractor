# Contents
# Acknowledgements
# Changes from Previous Versions
## Jan 1, 2025 - This Version
## Dec 4, 2023
## March 15, 2022
## January, 21, 2021
## December, 12, 2020
# Introduction
## Why This Book Exists
### What is Sustainability?
### Why Care About Sustainability?
### How to Value Sustainability
### Assumptions
#### The Software Has a Clear Purpose
#### The Software Needs To Exist For Years
#### The Software Will Evolve
#### The Team Will Change
#### You Value Sustainability, Consistency, and Quality
### Opportunity and Carrying Costs
### Why should you trust me?
## The Rails Application Architecture
### Boundaries
### Views
### Models
### Everything Else
### The Pros and Cons of the Rails Application Architecture
## Following Along in This Book
### Typographic Conventions
### Software Versions
### Sample Code
## Start Your App Off Right
### Creating a Rails App
### Using The Environment for Runtime Configuration
### Configuring Local Development Environment with dotenv
### Automating Application Setup with bin/setup
### Running the Application Locally with bin/dev
### Putting Tests and Other Quality Checks in bin/ci
### Improving Production Logging with lograge
## Business Logic (Does Not Go in Active Records)
### Business Logic Makes Your App Special…and Complex
#### Business Logic is a Magnet for Complexity
#### Business Logic Experiences Churn
### Bugs in Commonly-Used Classes Have Wide Effects
### Business Logic in Active Records Puts Churn and Complexity in Critical Classes
### Active Records Were Never Intended to Hold All the Business Logic
### Example Design of a Feature
# Deep Dive into Rails
## Routes and URLs
### Always Use Canonical Routes that Conform to Rails' Defaults
### Never Configure Routes That Aren't Being Used
### Vanity URLs Should Redirect to a Canonical Route
### Don't Create Custom Actions, Create More Resources
### Use Nested Routes Strategically
#### Create Sub-Resources Judiciously
#### Namespacing Might (or Might Not) be an Architecture Smell
### Nested Routes Can Organize Content Pages
## HTML Templates
### Use Semantic HTML
#### Build Views by Applying Meaningful Tags to Content
#### Use <div> and <span> for Styling
### Ideally, Expose One Instance Variable Per Action
#### Name the Instance Variable After the Resource
#### Reference Data, Global Context, and UI State are Exceptions
### Wrangling Partials for Simple View Re-use
#### Partials Allow Simple Code for Simple Re-use
#### Reference Only Locals in Partials
#### Partials Should Use Strict Locals
#### Use Default Values for Strict Locals to Simplify Partial APIs
### Use the View Component Library for Complex UI Logic
#### Creating a View Component
#### Testing Markup from a Unit Test
#### Deciding Between a Partial or a View Component
### Just Use ERB
## Helpers
### Don't Conflate Helpers with Your Domain
### Helpers are Best at Exposing Global UI State and Generating Markup
#### Global UI Logic and State
#### Small, Inline Components
### Configure Rails based on Your Strategy for Helpers
#### Consolidating Helpers in One File
#### Configure Helpers to Be Actually Modular
#### Use helper_method to Share Logic Between Views and Controllers
### Use Rails' APIs to Generate Markup
### Helpers Should Be Tested and Thus Testable
### Tackle Complex View Logic with Better Resource Design or View Components
#### Presenters Obscure Reality and Breed Inconsistency
#### Custom Resources and Active Model Create More Consistent Code
#### View Components can Render Entire Pages When Logic is Complex
## CSS
### Adopt a Design System
### Adopt a CSS Strategy
#### A CSS Framework
#### Object-Oriented CSS
#### Functional CSS
### Create a Living Style Guide to Document Your Design System and CSS Strategy
#### Do Not Underestimate the Carrying Cost of CSS
## Minimize JavaScript
### How and Why JavaScript is a Serious Liability
#### You Cannot Control The Runtime Environment
#### JavaScript's Behavior is Difficult to Observe
#### The Ecosystem Values Highly-Decoupled Modules that Favor Progress over Stability
### Embrace Server-Rendered Rails Views
#### Architecture of Rails Server-Rendered Views
#### Architecture of the JAM Stack
#### Server-Rendered Views by Default, JAM Stack Only When Needed
### Tweak Turbo to Provide a Slightly Better Experience
## Carefully Manage the JavaScript You Need
### Embrace the Web Platform for Basic Interactions
#### Sketching Out a Custom Element
#### Implementing the Custom Element
#### Custom Elements Age Well
### Carefully Choose One Framework When You Need It
### Ensure System Tests Fail When JavaScript is Broken
## Testing the View
### Understand the Value and Cost of Tests
### Use :rack_test for non-JavaScript User Flows
### Test Against Default Markup and Content Initially
### Cultivate Explicit Diagnostic Tools to Debug Test Failures
### Fake The Back-end To Get System Tests Passing
### Use data-testid Attributes to Combat Brittle Tests
### Test JavaScript Interactions with a Real Browser
#### Setting Up Headless Chrome
#### Writing a Browser-driven System Test Case
#### Enhancing with_clues to Dump Browser Logs
## Models, Part 1
### Active Record is for Database Access
#### Creating Some Example Active Records
#### Model the Database With Active Record's DSL
#### Class Methods Should Be Used to Re-use Common Database Operations
#### Instance Methods Should Implement Domain Concepts Derivable Directly from the Database
### Active Model is for Resource Modeling
## The Database
### Logical and Physical Data Models
### Create a Logical Model to Build Consensus
### Planning the Physical Model to Enforce Correctness
#### The Database Should Be Designed for Correctness
#### Use a SQL Schema
#### Use TIMESTAMP WITH TIME ZONE For Timestamps
#### Planning the Physical Model
### Creating Correct Migrations
#### Creating the Migration File and Helper Scripts
#### Iteratively Writing Migration Code to Create the Correct Schema
### Writing Tests for Database Constraints
## Business Logic Code is a Seam
### Business Logic Code Must Reveal Behavior
### Services are Stateless, Explicitly-Named Classes with Explicitly-Named Methods
#### A ThingDoer Class With a do_thing Method is Fine
#### Methods Receive Context and Data on Which to Operate, not Services to Delegate To
#### Return Rich Result Objects, not Booleans or Active Records
### Implementation Patterns You Might Want to Avoid
#### Creating Class Methods Closes Doors
#### ``Service Objects'' Using call Solve No Problem and Obscure Behavior
#### Dependency Injection also Obscures Behavior
## Models, Part 2
### Validations Don't Provide Data Integrity
#### Outside Code Naturally Skips Validations
#### Rails' Public API Allows Bypassing Validations
#### Some Validations Don't Technically Work
### Validations Are Awesome For User Experience
### How to (Barely) Use Callbacks
### Scopes are Often Business Logic and Belong Elsewhere
### Model Testing Strategy
#### Active Record Tests Should Test Database Constraints
#### Tests For Complex Validations or Callbacks
#### Ensure Anyone Can Create Valid Instances of the Model using Factory Bot
## End-to-End Example
### Example Requirements
### Building the UI First
#### Setting Up To Build the UI
#### Create Useful Seed Data for Development
#### Sketch the UI using Semantic Tags
#### Provide Basic Polish
#### Style the Form
#### Style Error States
### Writing a System Test
### Sketch Business Logic and Define the Seam
### Fully Implement and Test Business Logic
### Finished Implementation
## Controllers
### Controller Code is Configuration
### Don't Over-use Callbacks
### Controllers Should Convert Parameters to Richer Types
### Don't Over Test
#### Writing a Controller Test
#### Implementing a Basic Confidence-checking System
#### Avoiding Duplicative Tests
## Jobs
### Use Jobs To Defer Execution or Increase Fault-Tolerance
#### Web Workers, Worker Pools, Memory, and Compute Power
#### Network Calls and Third Parties are Slow
#### Network Calls and Third Parties are Flaky
#### Use Background Jobs Only When Needed
### Understand How Your Job Backend Works
#### Understand Where and How Jobs (and their Arguments) are Queued
#### Understand What Happens When a Job Fails
#### Observe the Behavior of Your Job Backend
### Sidekiq is The Best Job Backend for Most Teams
### Queue Jobs Directly, and Have Them Defer to Your Business Logic Code
#### Do Not Use Active Job - Use the Job Backend Directly
#### Job Code Should Defer to Your Service Layer
### Job Testing Strategies
### Jobs Will Get Retried and Must Be Idempotent
### Carefully Evaluate Solid Queue
#### There's No Reason (Yet) to Switch to Solid Queue
#### There Could Be Reasons to Use Solid Queue if You Manage Your Own Infrastructure
## Other Boundary Classes
### Mailers
#### Mailers Should Just Format Emails
#### Mailers are Usually Jobs
#### Previewing, Styling, and Checking your Mail
#### Using Mailcatcher to Allow Emails to be Sent in Development
### Rake Tasks
#### Rake Tasks Are For Automation
#### One Task Per File, Namespaces Match Directories
#### Rake Tasks Should Not Contain Business Logic
#### Prefer Ruby Command Line Apps for Developer Automation
### Mailboxes, Cables, and Active Storage
#### Action Mailbox
#### Action Cable
#### Active Storage
# Beyond Rails
## Authentication and Authorization
### When in Doubt Use Devise or OmniAuth
#### Use OmniAuth to Authenticate Using a Third Party
#### Building Authentication Into your App with Devise
### Authorization and Role-based Access Controls
#### Map Resources and Actions to Job Titles and Departments
#### Use Cancancan to Implement Role-Based Access
#### You Don't Have to Use All of Cancancan's Features
### Test Access Controls In System Tests
## API Endpoints
### Be Clear About What—and Who—Your API is For
### Write APIs the Same Way You Write Other Code
### Use the Simplest Authentication System You Can
### Use the Simplest Content Type You Can
### Just Put The Version in the URL
### Use .to_json to Create JSON
#### How Rails Renders JSON
#### Customizing JSON Serialization
#### Customize JSON in the Models Themselves
#### Always Use a Top Level Key
### Test API Endpoints
## Sustainable Process and Workflows
### Use Continuous Integration To Deploy
#### What is CI?
#### CI Configuration Should be Explicit and Managed
#### CI Should be Based on bin/setup and bin/ci
### Frequent Dependency Updates
#### Update Dependencies Early and Often
#### A Versioning Policy
#### Automate Dependency Updates
### Leverage Generators and Sample Repositories over Documentation
#### Create and Configure Rails Generators
#### Use Template Repositories for Ruby Gems and Rails Apps
### RubyGems and Railties Can Distribute Configuration
## Operations
### Why Observability Matters
### Monitor Business Outcomes
### Logging is Powerful
#### Include a Request ID in All Logs
#### Log What Something is and Where it Came From
#### Use Current to Include User IDs
### Manage Unhandled Exceptions
### Measure Performance
### Production Deployments Are For Professionals…Even if That's You
#### A Dockerfile Contains a Lot of Complexity
#### Kamal Gives You Both Control and Responsibility for Deployment
### Managing Secrets, Keys, and Passwords
# Appendices
## Setting Up Docker for Local Development
### Installing Docker
### What is Docker?
### Overview of the Environment
### Creating the Image
### Starting Up the Environment
### Executing Commands and Doing Development
### Customizing the Dev Environment
#### Installing Software
#### Copying Your Dotfiles Into the Image
## Monoliths, Microservices, and Shared Databases
### Monoliths Get a Bad Rap
### Microservices Are Not a Panacea.
### Sharing a Database Is Viable
## Technical Leadership is Critical
### Leadership Is About Shared Values
### Leaders Can be Held Accountable
### Accountability Can be Implicit
## Colophon