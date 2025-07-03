source "https://rubygems.org"

# Use Jekyll directly for GitHub Actions builds
gem "jekyll", "~> 4.3.0"

group :jekyll_plugins do
  gem "jekyll-optional-front-matter"
  gem "jekyll-readme-index"
  gem "jekyll-default-layout"
  gem "jekyll-titles-from-headings"
  gem "jekyll-relative-links"
  gem "jekyll-github-metadata"
  gem "jekyll-seo-tag"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
  gem "wdm", ">= 0.1.0" if Gem.win_platform?
end

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

# Required for Jekyll serve in Ruby 3.0+
gem "webrick"

# Required for Faraday retry middleware
gem "faraday-retry" 