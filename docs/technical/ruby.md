# Ruby

Ruby is a dynamic, object-oriented programming language known for its simplicity, productivity, and elegant syntax. It's widely used for web development, automation, and scripting.

## Installation and Setup

### Ruby Version Management with rbenv
```bash
# Install rbenv (macOS with Homebrew)
brew install rbenv ruby-build

# Install rbenv (Linux)
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash

# Add to shell profile
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Install latest Ruby
rbenv install 3.2.0
rbenv global 3.2.0

# Verify installation
ruby --version
gem --version
```

### Bundler and Gemfile
```ruby
# Gemfile
source 'https://rubygems.org'

ruby '3.2.0'

# Web framework
gem 'sinatra', '~> 3.0'
gem 'puma', '~> 6.0'

# Database
gem 'pg', '~> 1.4'
gem 'sequel', '~> 5.65'

# JSON handling
gem 'json', '~> 2.6'
gem 'multi_json', '~> 1.15'

# HTTP client
gem 'faraday', '~> 2.7'
gem 'httparty', '~> 0.21'

# Testing
group :test do
  gem 'rspec', '~> 3.12'
  gem 'rack-test', '~> 2.0'
  gem 'webmock', '~> 3.18'
  gem 'factory_bot', '~> 6.2'
end

# Development
group :development do
  gem 'rubocop', '~> 1.45'
  gem 'rubocop-rspec', '~> 2.18'
  gem 'pry', '~> 0.14'
  gem 'rerun', '~> 0.14'
end

# Utilities
gem 'dotenv', '~> 2.8'
gem 'logger', '~> 1.5'
gem 'redis', '~> 5.0'
```

```bash
# Install dependencies
bundle install

# Update gems
bundle update

# Execute with bundle context
bundle exec rspec
bundle exec rubocop
```

## Core Ruby Concepts

### Classes and Modules
```ruby
# Basic class definition
class User
  attr_reader :id, :email, :created_at
  attr_accessor :name, :age
  
  def initialize(id:, name:, email:, age: nil)
    @id = id
    @name = name
    @email = email
    @age = age
    @created_at = Time.now
  end
  
  def adult?
    @age && @age >= 18
  end
  
  def to_h
    {
      id: @id,
      name: @name,
      email: @email,
      age: @age,
      created_at: @created_at
    }
  end
  
  def to_json(*args)
    to_h.to_json(*args)
  end
  
  private
  
  def validate_email
    @email.match?(/\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i)
  end
end

# Module for mixins
module Timestampable
  def self.included(base)
    base.extend(ClassMethods)
  end
  
  module ClassMethods
    def with_timestamps
      attr_reader :created_at, :updated_at
      
      define_method :initialize do |*args, **kwargs|
        super(*args, **kwargs)
        @created_at = Time.now
        @updated_at = Time.now
      end
      
      define_method :touch do
        @updated_at = Time.now
      end
    end
  end
end

# Module for validation
module Validatable
  def valid?
    errors.empty?
  end
  
  def errors
    @errors ||= []
  end
  
  def add_error(message)
    errors << message
  end
  
  private
  
  def validate!
    errors.clear
    validate
    raise ValidationError, errors.join(', ') unless valid?
  end
  
  def validate
    # Override in including classes
  end
end

# Advanced class with mixins
class Order
  include Timestampable
  include Validatable
  
  with_timestamps
  
  attr_reader :id, :user_id, :items, :status
  attr_accessor :total_amount
  
  VALID_STATUSES = %w[pending processing shipped delivered cancelled].freeze
  
  def initialize(id:, user_id:, items: [], status: 'pending', total_amount: 0.0)
    @id = id
    @user_id = user_id
    @items = items
    @status = status
    @total_amount = total_amount
    super()
    validate!
  end
  
  def add_item(item)
    @items << item
    @total_amount += item[:price] * item[:quantity]
    touch
  end
  
  def status=(new_status)
    validate_status(new_status)
    @status = new_status
    touch
  end
  
  def pending?
    @status == 'pending'
  end
  
  def completed?
    @status == 'delivered'
  end
  
  private
  
  def validate
    add_error('User ID is required') if @user_id.nil? || @user_id.empty?
    add_error('Total amount must be positive') if @total_amount < 0
    validate_status(@status)
  end
  
  def validate_status(status)
    unless VALID_STATUSES.include?(status)
      add_error("Invalid status: #{status}")
    end
  end
end

# Usage examples
user = User.new(id: '123', name: 'John Doe', email: 'john@example.com', age: 25)
puts user.adult? # true
puts user.to_json

order = Order.new(
  id: 'order_123',
  user_id: user.id,
  items: [{ name: 'Book', price: 19.99, quantity: 2 }],
  total_amount: 39.98
)
order.add_item({ name: 'Pen', price: 2.99, quantity: 1 })
```

### Functional Programming Features
```ruby
# Blocks, Procs, and Lambdas
class DataProcessor
  def self.process_items(items, &block)
    items.map(&block)
  end
  
  def self.filter_items(items, &predicate)
    items.select(&predicate)
  end
  
  def self.create_multiplier(factor)
    ->(x) { x * factor }
  end
end

# Usage with blocks
numbers = [1, 2, 3, 4, 5]
doubled = DataProcessor.process_items(numbers) { |n| n * 2 }
evens = DataProcessor.filter_items(numbers, &:even?)

# Lambda usage
triple = DataProcessor.create_multiplier(3)
tripled = numbers.map(&triple)

# Method chaining and enumerable
users = [
  { name: 'Alice', age: 30, role: 'admin' },
  { name: 'Bob', age: 25, role: 'user' },
  { name: 'Charlie', age: 35, role: 'user' },
  { name: 'Diana', age: 28, role: 'admin' }
]

# Complex data transformations
admin_names = users
  .select { |user| user[:role] == 'admin' }
  .map { |user| user[:name] }
  .sort

average_age = users
  .map { |user| user[:age] }
  .reduce(:+) / users.length.to_f

# Group and aggregate
users_by_role = users.group_by { |user| user[:role] }
age_stats = users_by_role.transform_values do |group|
  ages = group.map { |user| user[:age] }
  {
    count: ages.length,
    average: ages.sum / ages.length.to_f,
    min: ages.min,
    max: ages.max
  }
end
```

## Web Development with Sinatra

### Basic API Server
```ruby
# app.rb
require 'sinatra'
require 'json'
require 'sequel'
require 'logger'
require 'dotenv'

Dotenv.load

# Database connection
DB = Sequel.connect(ENV['DATABASE_URL'] || 'postgres://localhost/myapp')

# Models
class User < Sequel::Model
  plugin :json_serializer
  plugin :validation_helpers
  plugin :timestamps
  
  one_to_many :orders
  
  def validate
    super
    validates_presence :name
    validates_format /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i, :email
    validates_unique :email
  end
  
  def to_api_hash
    {
      id: id,
      name: name,
      email: email,
      created_at: created_at,
      order_count: orders_dataset.count
    }
  end
end

class Order < Sequel::Model
  plugin :json_serializer
  plugin :validation_helpers
  plugin :timestamps
  
  many_to_one :user
  
  VALID_STATUSES = %w[pending processing shipped delivered cancelled].freeze
  
  def validate
    super
    validates_presence :user_id
    validates_includes VALID_STATUSES, :status
    validates_numeric :total_amount, only_integer: false
  end
  
  def to_api_hash
    {
      id: id,
      user_id: user_id,
      status: status,
      total_amount: total_amount.to_f,
      created_at: created_at,
      user: user&.to_api_hash
    }
  end
end

# Application configuration
configure do
  set :logger, Logger.new($stdout)
  set :show_exceptions, false
  set :raise_errors, false
end

# Middleware
before do
  content_type :json
  
  # Log requests
  logger.info "#{request.request_method} #{request.path_info}"
  
  # Parse JSON body
  if request.content_type&.include?('application/json')
    request.body.rewind
    @json_body = JSON.parse(request.body.read) rescue {}
  end
end

# Error handlers
error Sequel::ValidationFailed do |e|
  status 400
  { error: 'Validation failed', details: e.errors }.to_json
end

error Sequel::NoMatchingRow do
  status 404
  { error: 'Resource not found' }.to_json
end

error StandardError do |e|
  logger.error "Error: #{e.message}"
  logger.error e.backtrace.join("\n")
  
  status 500
  { error: 'Internal server error' }.to_json
end

# Routes
get '/health' do
  {
    status: 'healthy',
    timestamp: Time.now.iso8601,
    database: DB.test_connection ? 'connected' : 'disconnected'
  }.to_json
end

# User routes
get '/users' do
  page = (params[:page] || 1).to_i
  per_page = [(params[:per_page] || 20).to_i, 100].min
  
  users = User.limit(per_page, (page - 1) * per_page).all
  total = User.count
  
  {
    users: users.map(&:to_api_hash),
    meta: {
      page: page,
      per_page: per_page,
      total: total,
      pages: (total / per_page.to_f).ceil
    }
  }.to_json
end

get '/users/:id' do
  user = User[params[:id]]
  halt 404 unless user
  
  user.to_api_hash.to_json
end

post '/users' do
  user_params = @json_body.slice('name', 'email')
  user = User.create(user_params)
  
  status 201
  user.to_api_hash.to_json
end

put '/users/:id' do
  user = User[params[:id]]
  halt 404 unless user
  
  user_params = @json_body.slice('name', 'email')
  user.update(user_params)
  
  user.to_api_hash.to_json
end

delete '/users/:id' do
  user = User[params[:id]]
  halt 404 unless user
  
  user.destroy
  status 204
end

# Order routes
get '/users/:user_id/orders' do
  user = User[params[:user_id]]
  halt 404 unless user
  
  orders = user.orders_dataset.order(:created_at).all
  orders.map(&:to_api_hash).to_json
end

post '/users/:user_id/orders' do
  user = User[params[:user_id]]
  halt 404 unless user
  
  order_params = @json_body.slice('status', 'total_amount').merge(user_id: user.id)
  order = Order.create(order_params)
  
  status 201
  order.to_api_hash.to_json
end

# Global order routes
get '/orders' do
  status = params[:status]
  orders = Order.dataset
  orders = orders.where(status: status) if status
  
  orders.order(:created_at).all.map(&:to_api_hash).to_json
end

get '/orders/:id' do
  order = Order[params[:id]]
  halt 404 unless order
  
  order.to_api_hash.to_json
end

put '/orders/:id' do
  order = Order[params[:id]]
  halt 404 unless order
  
  order_params = @json_body.slice('status', 'total_amount')
  order.update(order_params)
  
  order.to_api_hash.to_json
end
```

### Background Jobs with Sidekiq
```ruby
# Gemfile addition
gem 'sidekiq', '~> 7.0'
gem 'sidekiq-web', '~> 0.0.9'

# config/sidekiq.rb
Sidekiq.configure_server do |config|
  config.redis = { url: ENV['REDIS_URL'] || 'redis://localhost:6379/0' }
end

Sidekiq.configure_client do |config|
  config.redis = { url: ENV['REDIS_URL'] || 'redis://localhost:6379/0' }
end

# app/workers/email_worker.rb
require 'sidekiq'

class EmailWorker
  include Sidekiq::Worker
  
  sidekiq_options retry: 3, queue: 'critical'
  
  def perform(user_id, email_type, options = {})
    user = User[user_id]
    return unless user
    
    case email_type
    when 'welcome'
      send_welcome_email(user, options)
    when 'order_confirmation'
      send_order_confirmation(user, options)
    when 'password_reset'
      send_password_reset(user, options)
    else
      logger.warn "Unknown email type: #{email_type}"
    end
  rescue StandardError => e
    logger.error "Failed to send #{email_type} email to user #{user_id}: #{e.message}"
    raise
  end
  
  private
  
  def send_welcome_email(user, options)
    logger.info "Sending welcome email to #{user.email}"
    # Email sending logic here
    EmailService.send_template(
      to: user.email,
      template: 'welcome',
      variables: { name: user.name }
    )
  end
  
  def send_order_confirmation(user, options)
    order_id = options['order_id']
    order = Order[order_id]
    
    logger.info "Sending order confirmation to #{user.email} for order #{order_id}"
    EmailService.send_template(
      to: user.email,
      template: 'order_confirmation',
      variables: {
        name: user.name,
        order_id: order.id,
        total: order.total_amount
      }
    )
  end
  
  def send_password_reset(user, options)
    token = options['token']
    
    logger.info "Sending password reset to #{user.email}"
    EmailService.send_template(
      to: user.email,
      template: 'password_reset',
      variables: {
        name: user.name,
        reset_url: "#{ENV['APP_URL']}/reset-password?token=#{token}"
      }
    )
  end
end

# Usage in application
post '/users' do
  user_params = @json_body.slice('name', 'email')
  user = User.create(user_params)
  
  # Enqueue welcome email
  EmailWorker.perform_async(user.id, 'welcome')
  
  status 201
  user.to_api_hash.to_json
end

post '/users/:user_id/orders' do
  user = User[params[:user_id]]
  halt 404 unless user
  
  order_params = @json_body.slice('status', 'total_amount').merge(user_id: user.id)
  order = Order.create(order_params)
  
  # Enqueue order confirmation email
  EmailWorker.perform_async(user.id, 'order_confirmation', { order_id: order.id })
  
  status 201
  order.to_api_hash.to_json
end
```

## Database Operations with Sequel

### Advanced Database Usage
```ruby
# config/database.rb
require 'sequel'
require 'logger'

class DatabaseConfig
  def self.setup
    db_url = ENV['DATABASE_URL'] || 'postgres://localhost/myapp'
    
    DB = Sequel.connect(db_url, {
      max_connections: ENV.fetch('DB_POOL_SIZE', 10).to_i,
      pool_timeout: 30,
      logger: Logger.new($stdout),
      sql_log_level: :debug
    })
    
    # Enable extensions
    DB.extension :pg_json
    DB.extension :pg_array
    DB.extension :connection_validator
    DB.extension :health_check
    
    # Set up connection validation
    DB.pool.connection_validation_timeout = 3600
    
    DB
  end
end

# Migration example
Sequel.migration do
  up do
    create_table(:users) do
      primary_key :id
      String :name, null: false
      String :email, null: false, unique: true
      Integer :age
      column :roles, 'text[]', default: Sequel.pg_array(['user'])
      column :metadata, :jsonb, default: Sequel.pg_json({})
      DateTime :created_at, default: Sequel::CURRENT_TIMESTAMP
      DateTime :updated_at, default: Sequel::CURRENT_TIMESTAMP
      
      index :email
      index :created_at
    end
    
    create_table(:orders) do
      primary_key :id
      foreign_key :user_id, :users, null: false, on_delete: :cascade
      BigDecimal :total_amount, size: [10, 2], null: false
      String :status, default: 'pending'
      column :items, :jsonb, default: Sequel.pg_json([])
      DateTime :created_at, default: Sequel::CURRENT_TIMESTAMP
      DateTime :updated_at, default: Sequel::CURRENT_TIMESTAMP
      
      index [:user_id, :created_at]
      index :status
      index :created_at
    end
  end
  
  down do
    drop_table(:orders)
    drop_table(:users)
  end
end

# Advanced model with hooks and validations
class User < Sequel::Model
  plugin :json_serializer
  plugin :validation_helpers
  plugin :timestamps, update_on_create: true
  plugin :dirty
  plugin :caching
  
  one_to_many :orders
  
  dataset_module do
    def by_role(role)
      where(Sequel.pg_array(:roles).contains([role]))
    end
    
    def active
      where(status: 'active')
    end
    
    def recent(days = 30)
      where { created_at > Date.today - days }
    end
    
    def with_orders
      eager(:orders)
    end
  end
  
  def validate
    super
    validates_presence [:name, :email]
    validates_format /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i, :email
    validates_unique :email
    validates_integer :age, allow_nil: true
    validates_includes %w[active inactive suspended], :status, allow_nil: true
  end
  
  def before_create
    super
    self.status ||= 'active'
    add_role('user') unless has_role?('user')
  end
  
  def before_update
    super
    self.updated_at = Time.now
  end
  
  def after_create
    super
    UserCreatedEvent.publish(self)
  end
  
  def add_role(role)
    self.roles = (roles + [role]).uniq
  end
  
  def remove_role(role)
    self.roles = roles - [role]
  end
  
  def has_role?(role)
    roles.include?(role)
  end
  
  def admin?
    has_role?('admin')
  end
  
  def total_spent
    orders_dataset.sum(:total_amount) || 0
  end
  
  def recent_orders(limit = 10)
    orders_dataset.order(Sequel.desc(:created_at)).limit(limit)
  end
  
  def to_api_hash(include_sensitive: false)
    hash = {
      id: id,
      name: name,
      email: include_sensitive ? email : email.gsub(/(?<=.{2}).(?=.*@)/, '*'),
      age: age,
      roles: roles,
      status: status,
      total_spent: total_spent,
      order_count: orders.count,
      created_at: created_at,
      updated_at: updated_at
    }
    
    hash[:metadata] = metadata if include_sensitive
    hash
  end
end

# Repository pattern for complex queries
class UserRepository
  def self.find_active_users_with_recent_orders(days = 30)
    User.dataset
        .where(status: 'active')
        .where { created_at > Date.today - days }
        .eager_graph(:orders)
        .where { orders__created_at > Date.today - days }
        .all
  end
  
  def self.user_statistics
    DB[:users]
      .select_group(:status)
      .select_append { count.function.*.as(user_count) }
      .select_append { avg(:age).as(average_age) }
      .to_hash_groups(:status)
  end
  
  def self.top_spenders(limit = 10)
    DB[:users]
      .join(:orders, user_id: :id)
      .group(:users__id, :users__name, :users__email)
      .select(:users__id, :users__name, :users__email)
      .select_append { sum(:orders__total_amount).as(total_spent) }
      .select_append { count(:orders__id).as(order_count) }
      .order(Sequel.desc(:total_spent))
      .limit(limit)
      .all
  end
  
  def self.bulk_update_roles(user_ids, new_roles)
    DB.transaction do
      User.where(id: user_ids).update(roles: Sequel.pg_array(new_roles))
    end
  end
end
```

## Testing with RSpec

### Test Setup and Configuration
```ruby
# spec/spec_helper.rb
require 'rack/test'
require 'rspec'
require 'webmock/rspec'
require 'factory_bot'
require 'database_cleaner'

ENV['RACK_ENV'] = 'test'

require_relative '../app'

RSpec.configure do |config|
  config.include Rack::Test::Methods
  config.include FactoryBot::Syntax::Methods
  
  # Database cleaner setup
  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end
  
  config.around(:each) do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end
  
  # Disable external HTTP requests
  config.before(:each) do
    WebMock.disable_net_connect!(allow_localhost: true)
  end
  
  def app
    Sinatra::Application
  end
end

# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    sequence(:name) { |n| "User #{n}" }
    sequence(:email) { |n| "user#{n}@example.com" }
    age { rand(18..80) }
    roles { ['user'] }
    status { 'active' }
    
    trait :admin do
      roles { ['user', 'admin'] }
    end
    
    trait :with_orders do
      after(:create) do |user|
        create_list(:order, 3, user: user)
      end
    end
    
    trait :inactive do
      status { 'inactive' }
    end
  end
  
  factory :order do
    association :user
    total_amount { BigDecimal(rand(10.0..1000.0).round(2).to_s) }
    status { 'pending' }
    items { [{ name: 'Product', quantity: 1, price: total_amount }] }
    
    trait :completed do
      status { 'delivered' }
    end
    
    trait :high_value do
      total_amount { BigDecimal('1000.00') }
    end
  end
end
```

### Unit and Integration Tests
```ruby
# spec/models/user_spec.rb
require 'spec_helper'

RSpec.describe User do
  describe 'validations' do
    it 'requires a name' do
      user = build(:user, name: nil)
      expect(user).not_to be_valid
      expect(user.errors[:name]).to include("is not present")
    end
    
    it 'requires a valid email' do
      user = build(:user, email: 'invalid-email')
      expect(user).not_to be_valid
      expect(user.errors[:email]).to include("is invalid")
    end
    
    it 'requires unique email' do
      create(:user, email: 'test@example.com')
      user = build(:user, email: 'test@example.com')
      expect(user).not_to be_valid
      expect(user.errors[:email]).to include("is already taken")
    end
  end
  
  describe 'roles' do
    let(:user) { create(:user) }
    
    it 'adds user role by default' do
      expect(user.has_role?('user')).to be true
    end
    
    it 'can add roles' do
      user.add_role('admin')
      user.save
      expect(user.has_role?('admin')).to be true
    end
    
    it 'can remove roles' do
      user.add_role('admin')
      user.save
      user.remove_role('admin')
      user.save
      expect(user.has_role?('admin')).to be false
    end
    
    it 'prevents duplicate roles' do
      user.add_role('admin')
      user.add_role('admin')
      expect(user.roles.count('admin')).to eq 1
    end
  end
  
  describe 'associations' do
    it 'can have many orders' do
      user = create(:user, :with_orders)
      expect(user.orders.count).to eq 3
    end
    
    it 'calculates total spent' do
      user = create(:user)
      create(:order, user: user, total_amount: 100)
      create(:order, user: user, total_amount: 200)
      
      expect(user.total_spent).to eq 300
    end
  end
  
  describe '#to_api_hash' do
    let(:user) { create(:user, email: 'test@example.com') }
    
    it 'masks email by default' do
      hash = user.to_api_hash
      expect(hash[:email]).to eq 'te**@example.com'
    end
    
    it 'includes full email when requested' do
      hash = user.to_api_hash(include_sensitive: true)
      expect(hash[:email]).to eq 'test@example.com'
    end
    
    it 'includes computed fields' do
      hash = user.to_api_hash
      expect(hash).to include(:total_spent, :order_count)
    end
  end
end

# spec/api/users_spec.rb
require 'spec_helper'

RSpec.describe 'Users API' do
  describe 'GET /users' do
    before do
      create_list(:user, 15)
    end
    
    it 'returns paginated users' do
      get '/users'
      
      expect(last_response).to be_ok
      
      json = JSON.parse(last_response.body)
      expect(json['users'].length).to eq 15
      expect(json['meta']['total']).to eq 15
      expect(json['meta']['page']).to eq 1
    end
    
    it 'supports pagination' do
      get '/users?page=2&per_page=5'
      
      expect(last_response).to be_ok
      
      json = JSON.parse(last_response.body)
      expect(json['users'].length).to eq 5
      expect(json['meta']['page']).to eq 2
      expect(json['meta']['per_page']).to eq 5
    end
    
    it 'limits per_page to 100' do
      get '/users?per_page=200'
      
      json = JSON.parse(last_response.body)
      expect(json['meta']['per_page']).to eq 100
    end
  end
  
  describe 'POST /users' do
    let(:valid_params) do
      {
        name: 'John Doe',
        email: 'john@example.com'
      }
    end
    
    it 'creates a new user' do
      post '/users', valid_params.to_json, { 'CONTENT_TYPE' => 'application/json' }
      
      expect(last_response.status).to eq 201
      
      json = JSON.parse(last_response.body)
      expect(json['name']).to eq 'John Doe'
      expect(json['email']).to eq 'jo**@example.com'
    end
    
    it 'validates required fields' do
      post '/users', {}.to_json, { 'CONTENT_TYPE' => 'application/json' }
      
      expect(last_response.status).to eq 400
      
      json = JSON.parse(last_response.body)
      expect(json['error']).to eq 'Validation failed'
      expect(json['details']).to include('name')
    end
    
    it 'prevents duplicate emails' do
      create(:user, email: 'john@example.com')
      
      post '/users', valid_params.to_json, { 'CONTENT_TYPE' => 'application/json' }
      
      expect(last_response.status).to eq 400
      
      json = JSON.parse(last_response.body)
      expect(json['details']).to include('email')
    end
  end
  
  describe 'GET /users/:id' do
    let(:user) { create(:user) }
    
    it 'returns user details' do
      get "/users/#{user.id}"
      
      expect(last_response).to be_ok
      
      json = JSON.parse(last_response.body)
      expect(json['id']).to eq user.id
      expect(json['name']).to eq user.name
    end
    
    it 'returns 404 for non-existent user' do
      get '/users/999999'
      
      expect(last_response.status).to eq 404
      
      json = JSON.parse(last_response.body)
      expect(json['error']).to eq 'Resource not found'
    end
  end
end
```

### Background Job Testing
```ruby
# spec/workers/email_worker_spec.rb
require 'spec_helper'
require 'sidekiq/testing'

RSpec.describe EmailWorker do
  let(:user) { create(:user) }
  
  before do
    Sidekiq::Testing.fake!
  end
  
  after do
    Sidekiq::Worker.clear_all
  end
  
  describe 'enqueuing' do
    it 'enqueues welcome email job' do
      expect {
        EmailWorker.perform_async(user.id, 'welcome')
      }.to change(EmailWorker.jobs, :size).by(1)
    end
    
    it 'sets correct queue' do
      EmailWorker.perform_async(user.id, 'welcome')
      expect(EmailWorker.jobs.last['queue']).to eq 'critical'
    end
  end
  
  describe 'processing' do
    before do
      Sidekiq::Testing.inline!
      allow(EmailService).to receive(:send_template)
    end
    
    it 'sends welcome email' do
      EmailWorker.perform_async(user.id, 'welcome')
      
      expect(EmailService).to have_received(:send_template).with(
        to: user.email,
        template: 'welcome',
        variables: { name: user.name }
      )
    end
    
    it 'sends order confirmation email' do
      order = create(:order, user: user)
      
      EmailWorker.perform_async(user.id, 'order_confirmation', { 'order_id' => order.id })
      
      expect(EmailService).to have_received(:send_template).with(
        to: user.email,
        template: 'order_confirmation',
        variables: {
          name: user.name,
          order_id: order.id,
          total: order.total_amount
        }
      )
    end
    
    it 'handles unknown email types gracefully' do
      expect {
        EmailWorker.perform_async(user.id, 'unknown_type')
      }.not_to raise_error
    end
    
    it 'handles missing users gracefully' do
      expect {
        EmailWorker.perform_async(999999, 'welcome')
      }.not_to raise_error
      
      expect(EmailService).not_to have_received(:send_template)
    end
  end
end
```

## Best Practices and Patterns

### Service Objects
```ruby
# app/services/user_registration_service.rb
class UserRegistrationService
  include ActiveModel::Validations
  
  attr_reader :params, :user, :errors
  
  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :name, presence: true, length: { minimum: 2 }
  validates :password, presence: true, length: { minimum: 8 }
  
  def initialize(params)
    @params = params.transform_keys(&:to_sym)
    @errors = []
  end
  
  def call
    return failure('Invalid parameters') unless valid?
    
    DB.transaction do
      create_user
      send_welcome_email
      log_registration
    end
    
    success(user)
  rescue Sequel::ValidationFailed => e
    failure("Registration failed: #{e.message}")
  rescue StandardError => e
    failure("Unexpected error: #{e.message}")
  end
  
  def success?
    @success == true
  end
  
  private
  
  def create_user
    @user = User.create(
      name: params[:name],
      email: params[:email],
      password_hash: BCrypt::Password.create(params[:password])
    )
  end
  
  def send_welcome_email
    EmailWorker.perform_async(user.id, 'welcome')
  end
  
  def log_registration
    logger.info "User registered: #{user.id} (#{user.email})"
  end
  
  def success(data)
    @success = true
    @result = data
  end
  
  def failure(message)
    @success = false
    @errors << message
    nil
  end
  
  def logger
    @logger ||= Logger.new($stdout)
  end
end

# Usage
service = UserRegistrationService.new(
  name: 'John Doe',
  email: 'john@example.com',
  password: 'secure123'
)

if service.call
  puts "User created: #{service.user.id}"
else
  puts "Registration failed: #{service.errors.join(', ')}"
end
```

### Configuration Management
```ruby
# config/application.rb
class Application
  class << self
    def config
      @config ||= Configuration.new
    end
    
    def configure
      yield(config)
    end
    
    def environment
      ENV['RACK_ENV'] || 'development'
    end
    
    def development?
      environment == 'development'
    end
    
    def production?
      environment == 'production'
    end
    
    def test?
      environment == 'test'
    end
  end
  
  class Configuration
    attr_accessor :database_url, :redis_url, :log_level, :session_secret,
                  :email_service, :file_storage, :cache_ttl
    
    def initialize
      # Default values
      @log_level = :info
      @cache_ttl = 3600
      @email_service = :sendgrid
      @file_storage = :local
      
      # Load from environment
      load_from_env
    end
    
    private
    
    def load_from_env
      @database_url = ENV['DATABASE_URL']
      @redis_url = ENV['REDIS_URL']
      @session_secret = ENV['SESSION_SECRET']
      @log_level = ENV['LOG_LEVEL']&.to_sym || @log_level
      @cache_ttl = ENV['CACHE_TTL']&.to_i || @cache_ttl
    end
  end
end

# Usage
Application.configure do |config|
  config.database_url = 'postgres://localhost/myapp'
  config.log_level = :debug if Application.development?
end
```

## Resources

- [Ruby Documentation](https://ruby-doc.org/)
- [RubyGems Package Manager](https://rubygems.org/)
- [Bundler Dependency Manager](https://bundler.io/)
- [Sinatra Web Framework](http://sinatrarb.com/)
- [Sequel ORM](https://sequel.jeremyevans.net/)
- [RSpec Testing Framework](https://rspec.info/)
- [Sidekiq Background Jobs](https://sidekiq.org/)
- [Ruby Style Guide](https://rubystyle.guide/)
- [Effective Ruby Book](https://www.effectiveruby.com/)
- [Ruby Weekly Newsletter](https://rubyweekly.com/)