module Jekyll
  class PracticeSetGenerator < Generator
    safe true

    def generate(site)
      module_code_map = {
        'm1r5' => ['m1r5', 'm1r5-practice', 'm1r5-comprehensive'],
        'm2r5' => ['m2r5', 'm2r5-practice', 'm2r5-comprehensive'],
        'm3r5' => ['m3r5', 'm3r5-practice', 'm3r5-comprehensive'],
        'm4r5' => ['m4r5', 'm4r5-practice', 'm4r5-comprehensive'],
      }

      # Load UI text from modules_data.yml
      modules_data_path = File.join(site.source, '_data', 'modules_data.yml')
      modules_data = YAML.load_file(modules_data_path)
      ui = modules_data['ui_text'] || {}

      # Load course modules for code->title mapping
      course_modules_path = File.join(site.source, '_data', 'course_modules.yml')
      course_modules = YAML.load_file(course_modules_path)
      code_to_title = {}
      (course_modules['modules'] || []).each do |mod|
        code_to_title[mod['code']] = mod['title']
      end

      # Load module UI info (icon, color) from modules_data.yml
      module_ui_map = {}
      (modules_data['modules'] || {}).each do |k, v|
        code = v['code'] || k.downcase
        module_ui_map[code] = { 'icon' => v['icon'], 'color' => v['color'] }
      end

      # Find all practice data files (regular and comprehensive)
      practice_files = [
        'm1r5_practice', 'm2r5_practice', 'm3r5_practice', 'm4r5_practice',
        'm5r5_practice', 'm6r5_practice', 'm7r5_practice',
        'm1r5_comprehensive', 'm2r5_comprehensive', 'm3r5_comprehensive', 'm4r5_comprehensive',
        'm5r5_comprehensive', 'm6r5_comprehensive', 'm7r5_comprehensive',
        'match_together_questions', 'multiple_answer_questions'
      ]
      
      practice_files.each do |file_key|
        next unless site.data.key?(file_key)
        
        data = site.data[file_key]
        next unless data.is_a?(Hash) && data.key?('sets')
        
        # --- Generate main practice list page (if not comprehensive) ---
        if file_key.match(/_practice$/)
          module_match = file_key.match(/^(m\d)r(\d)/)
          if module_match
            code = "#{module_match[1]}r#{module_match[2]}"
            module_name = code
            module_title = code_to_title[code] || code
            page_dir = "#{code}/#{code}-practice"

            # --- NEW: Load comprehensive sets if available ---
            comp_file_key = file_key.sub('_practice', '_comprehensive')
            comp_sets = []
            if site.data.key?(comp_file_key) && site.data[comp_file_key].is_a?(Hash) && site.data[comp_file_key].key?('sets')
              comp_sets = site.data[comp_file_key]['sets']
            end

            # Generate the main practice list page with a custom layout and sets array
            list_page = PracticeSetPage.new(site, site.source, page_dir, data, module_name, false, ui, code_to_title, module_title, module_ui_map[code] ? module_ui_map[code]['icon'] : nil, module_ui_map[code] ? module_ui_map[code]['color'] : nil)
            list_page.data['layout'] = 'practice_list'
            list_page.data['practice_sets'] = data['sets']
            list_page.data['comprehensive_sets'] = comp_sets
            list_page.data.delete('practice_set')
            list_page.data['module_name'] = code
            list_page.data['module_title'] = module_title
            site.pages << list_page
          end
        end
        # --- End main practice list page generation ---
        
        data['sets'].each do |set_info|
          # Extract module name for module-specific files
          module_name = nil
          is_comprehensive = false
          page_dir = nil
          module_title = nil
          
          if file_key.match(/^(m\d)r(\d)/)
            module_match = file_key.match(/^(m\d)r(\d)/)
            code = "#{module_match[1]}r#{module_match[2]}"
            module_name = code
            module_title = code_to_title[code] || code
            is_comprehensive = file_key.include?('comprehensive')
            if is_comprehensive
              page_dir = "#{code}/#{code}-comprehensive/#{code}-comprehensive-#{set_info['id']}"
            else
              page_dir = "#{code}/#{code}-practice/#{code}-practice-#{set_info['id']}"
            end
          else
            # For question type files like match_together_questions and multiple_answer_questions
            question_type = file_key.gsub('_questions', '').capitalize
            module_name = question_type
            module_title = question_type
            page_dir = "question-types/#{file_key.gsub('_', '-')}/#{file_key.gsub('_', '-')}-#{set_info['id']}"
          end

          # Determine module icon and color
          module_icon = nil
          module_color = nil
          if module_ui_map[module_name]
            module_icon = module_ui_map[module_name]['icon']
            module_color = module_ui_map[module_name]['color']
          end

          # --- Normalize questions ---
          if set_info['questions'].is_a?(Array)
            set_info['questions'] = set_info['questions'].map do |q|
              choices_arr = if q['type'] == 'match' && q['choices'].is_a?(Array)
                q['choices']
              elsif q['choices'].is_a?(Hash) && !q['choices'].empty?
                q['choices'].map { |letter, text| { 'letter' => letter, 'text' => text } }
              else
                []
              end
              type = q['type']
              answer = q['answer']
              if type == 'match'
                # keep type as 'match'
              elsif type == 'multiple' || answer.is_a?(Array)
                type = 'multiple'
                answer = Array(answer)
              end
              normalized_q = q.dup
              normalized_q['choices'] = choices_arr
              normalized_q['answer'] = answer
              normalized_q['type'] = type
              normalized_q['explanation'] = q['explanation']
              normalized_q['indicator'] = q['indicator'] if q.key?('indicator')
              normalized_q.delete_if { |_, v| v.nil? }
              normalized_q
            end
          end
          set_info['questions'] ||= []

          # Always generate a per-set page with the 'practice' layout and the set as 'practice_set'
          set_page = PracticeSetPage.new(site, site.source, page_dir, set_info, module_name, is_comprehensive, ui, code_to_title, module_title, module_icon, module_color)
          set_page.data['layout'] = 'practice'
          set_page.data['practice_set'] = set_info
          site.pages << set_page
        end
      end

      # --- NEW: Generate module overview pages dynamically ---
      course_modules_path = File.join(site.source, '_data', 'course_modules.yml')
      course_modules = YAML.load_file(course_modules_path)
      modules_data_path = File.join(site.source, '_data', 'modules_data.yml')
      modules_data = YAML.load_file(modules_data_path)
      ui = modules_data['ui_text'] || {}
      module_ui_map = modules_data['modules'] || {}

      (course_modules['modules'] || []).each do |mod|
        next unless mod['visible']
        code = mod['code']
        # Find UI info (icon, color) for this module
        ui_info = module_ui_map.values.find { |v| v['code'] == code }
        icon = ui_info ? ui_info['icon'] : nil
        color = ui_info ? ui_info['color'] : nil
        # Path: /[module-code]/index.html
        page_dir = code
        overview_page = ModuleOverviewPage.new(site, site.source, page_dir, mod, ui, icon, color)
        overview_page.data['layout'] = 'default'
        overview_page.data['title'] = mod['title']
        overview_page.data['permalink'] = "/#{code}/"
        site.pages << overview_page
      end
      # --- END module overview generation ---
    end
  end

  class PracticeSetPage < Page
    def initialize(site, base, dir, practice_set, module_name, is_comprehensive = false, ui = {}, code_to_title = {}, module_title = nil, module_icon = nil, module_color = nil)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      
      # Set page data
      self.data = {}
      self.data['layout'] = 'practice'
      self.data['module_icon'] = module_icon
      self.data['module_color'] = module_color
      
      # Set title based on whether it's comprehensive, module-specific, or question type
      if module_name.match(/^(m1r5|m2r5|m3r5|m4r5)$/)
        full_title = module_title ? "#{module_name}: #{module_title}" : module_name
        if is_comprehensive
          banner_title = ui['comprehensive_banner_title'].to_s.strip
          banner_title = 'Comprehensive Practice Set' if banner_title.empty?
          self.data['title'] = "#{full_title} #{banner_title} ##{practice_set['id']}"
          # Add set_info_text for comprehensive sets, matching the non-comprehensive sentence style
          module_set_contains = (ui['module_set_contains'] || 'Practice Set').gsub('%{module}', full_title)
          self.data['set_info_text'] = "#{module_set_contains} ##{practice_set['id']}"
        else
          module_set_contains = (ui['module_set_contains'] || 'Practice Set').gsub('%{module}', full_title)
          self.data['title'] = full_title
          self.data['set_info_text'] = "#{module_set_contains} ##{practice_set['id']}"
        end
      else
        # Question type title
        self.data['title'] = "#{ui['question_type_banner_title'] ? ui['question_type_banner_title'].gsub('%{type}', module_name) : 'Practice Set'} ##{practice_set['id']}"
      end
      
      self.data['practice_set'] = practice_set
      self.data['is_comprehensive'] = is_comprehensive
      self.data['module_name'] = module_name
      self.data['module_title'] = module_title
      
      # Set content
      self.content = generate_content(module_name, is_comprehensive, practice_set, ui, module_title, module_icon, module_color)
    end

    private

    def generate_content(module_name, is_comprehensive, practice_set, ui, module_title = nil, module_icon = nil, module_color = nil)
      content = ""
      banner_style = module_color ? " style='background: #{module_color};'" : ""
      icon_html = module_icon ? "<span class='material-symbols-outlined'>#{module_icon}</span>" : "<span class='material-symbols-outlined'>info</span>"
      # Banner for comprehensive or question type sets
      if is_comprehensive
        content << "<section class='set-info-banner modern-banner'#{banner_style}>"
        content << "<div class='banner-icon'>#{icon_html}</div>"
        content << "<div class='banner-content'>"
        content << "<h2>#{ui['comprehensive_banner_title'] || 'Comprehensive Practice Set'}</h2>"
        content << "<p>#{ui['comprehensive_banner_desc'] || 'This is a full-length practice set simulating actual exam conditions.'}</p>"
        content << "<ul class='banner-details'>"
        content << "<li><strong>#{ui['total_questions'] || 'Total Questions'}:</strong> #{(practice_set['questions'] || []).size}</li>"
        content << "<li><strong>#{ui['duration'] || 'Duration'}:</strong> #{practice_set['duration_minutes']} minutes</li>"
        content << "</ul>"
        content << "</div>"
        content << "</section>"
      elsif !module_name.match(/^(m1r5|m2r5|m3r5|m4r5)$/)
        banner_title = ui['question_type_banner_title']&.gsub('%{type}', module_name) || "#{module_name} Questions"
        banner_desc = ui['question_type_banner_desc']&.gsub('%{type}', module_name.downcase) || "This practice set focuses on #{module_name.downcase} questions."
        content << "<section class='set-info-banner modern-banner'#{banner_style}>"
        content << "<div class='banner-icon'>#{icon_html}</div>"
        content << "<div class='banner-content'>"
        content << "<h2>#{banner_title}</h2>"
        content << "<p>#{banner_desc}</p>"
        content << "<ul class='banner-details'>"
        content << "<li><strong>#{ui['total_questions'] || 'Total Questions'}:</strong> #{(practice_set['questions'] || []).size}</li>"
        content << "<li><strong>#{ui['duration'] || 'Duration'}:</strong> #{practice_set['duration_minutes']} minutes</li>"
        content << "</ul>"
        content << "</div>"
        content << "</section>"
      end

      # Info text for module or type
      if module_name.match(/^(m1r5|m2r5|m3r5|m4r5)$/)
        info_text = ui['module_set_contains']&.gsub('%{module}', module_name) || "This practice set contains questions for #{module_name}."
      else
        info_text = ui['type_set_contains']&.gsub('%{type}', module_name.downcase) || "This practice set contains #{module_name.downcase} questions."
      end
      select_answer = ui['select_answer'] || 'Select your answer for each question to see immediate feedback.'
      one_per_page = ui['one_per_page'] || 'Questions are shown one per page. Use the navigation buttons to move between pages.'
      content << "<div class='practice-info modern-card'><p>#{info_text} #{select_answer}</p>\n<p>#{one_per_page}</p></div>\n"

      # Practice features
      content << "<ul class='practice-features modern-card'>"
      content << "<li><span class='material-symbols-outlined'>check_circle</span> Topic-specific practice sets</li>"
      content << "<li><span class='material-symbols-outlined'>check_circle</span> Full-length comprehensive sets</li>"
      content << "<li><span class='material-symbols-outlined'>check_circle</span> Simulated exam conditions with time limits</li>"
      content << "</ul>"

      # Exam tips for comprehensive sets
      if is_comprehensive
        content << "<section class='exam-tips modern-card modern-tips'>"
        content << "<div class='tips-header'><span class='material-symbols-outlined'>lightbulb</span> <strong>#{ui['exam_tips_header'] || 'Exam Tips'}</strong></div>"
        content << "<ul class='tips-list'>"
        exam_tips = ui['exam_tips'] || [
          'Manage your time wisely - you have %{minutes} minutes for %{questions} questions',
          'Read each question carefully before answering',
          "Don\'t spend too much time on any single question",
          'Review your answers if time permits'
        ]
        exam_tips.each do |tip|
          tip = tip.gsub('%{minutes}', practice_set['duration_minutes'].to_s).gsub('%{questions}', (practice_set['questions'] || []).size.to_s)
          content << "<li>#{tip}</li>"
        end
        content << "</ul>"
        content << "</section>"
      end

      content
    end
  end

  class ModuleOverviewPage < Page
    def initialize(site, base, dir, module_data, ui, icon, color)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'
      self.process(@name)
      self.data = {}
      self.data['module'] = module_data
      self.data['icon'] = icon
      self.data['color'] = color
      self.data['ui'] = ui
      self.content = generate_content(module_data, ui, icon, color)
    end

    private
    def generate_content(module_data, ui, icon, color)
      # HTML structure based on static /pages/M1-R5.html
      practice_url = "#{@site.config['baseurl']}".chomp('/') + "/#{module_data['code']}/#{module_data['code'].gsub('-', '')}-practice/"
      banner_style = color ? " style='background: #{color};'" : ''
      icon_html = icon ? "<span class='material-symbols-outlined'>#{icon}</span>" : ''
      <<~HTML
      <div class="module-page">
        <div class="module-title-container">
          <h1>#{module_data['title']}</h1>
          <a href="#{practice_url}" class="practice-link-icon" title="Practice Questions">
            <span class="material-symbols-outlined">assignment_turned_in</span>
          </a>
        </div>
        <div class="module-content">
          <section class="module-description">
            <h2>#{ui['overview_header'] || 'Overview'}</h2>
            <p>#{module_data['description']}</p>
            <p class="syllabus-ref">
              #{ui['syllabus_ref']}
              <a href="#{ui['openagi_news_url']}" target="_blank">
                #{ui['resource_link_text']}
              </a>
            </p>
          </section>
          <section class="practice-cta">
            <div class="practice-card">
              <div class="practice-icon">
                <span class="material-symbols-outlined">quiz</span>
              </div>
              <div class="practice-content">
                <h3>Ready to Test Your Knowledge?</h3>
                <p>Practice with our comprehensive question sets designed to help you master #{module_data['title']} concepts.</p>
                <ul class="practice-features">
                  <li><span class="material-symbols-outlined">check_circle</span> Topic-specific practice sets</li>
                  <li><span class="material-symbols-outlined">check_circle</span> Full-length comprehensive sets</li>
                  <li><span class="material-symbols-outlined">check_circle</span> Simulated exam conditions with time limits</li>
                </ul>
                <a href="#{practice_url}" class="practice-btn">
                  <span class="material-symbols-outlined">play_arrow</span>
                  Start Practice Sets
                </a>
              </div>
            </div>
          </section>
          <section class="course-outline">
            <h2>#{ui['outline_header'] || 'Course Outline'}</h2>
            <table class="outline-table">
              <thead>
                <tr><th>S.No</th><th>Topic</th><th>Written Marks (Max.)</th></tr>
              </thead>
              <tbody>
                #{(module_data['topics'] || []).each_with_index.map { |topic, i| "<tr><td>#{i+1}.</td><td>#{topic['name']}</td><td>#{topic['marks']}</td></tr>" }.join}
              </tbody>
            </table>
          </section>
          <section class="detailed-topics">
            <h2>#{ui['detailed_topics_header'] || 'Detailed Topics'}</h2>
            <div class="topics-grid">
              #{(module_data['key_topics'] || []).map { |kt| "<div class='topic-card'><h3>#{kt['name']}</h3><ul>#{(kt['subtopics'] || []).map { |st| "<li>#{st}</li>" }.join}</ul></div>" }.join}
            </div>
          </section>
          <section class="study-resources">
            <h2>#{ui['resources_header'] || 'Resources'}</h2>
            <a href="#{ui['openagi_news_url']}" target="_blank">#{ui['resource_link_text']}</a>
          </section>
        </div>
      </div>
      <style>
        .practice-features {
          list-style: none;
          padding: 0;
          margin: 15px 0;
        }
        .practice-features li {
          display: flex;
          align-items: center;
          margin-bottom: 8px;
          color: var(--md-on-surface-variant, #666);
          font-size: 0.9em;
          transition: color 0.3s;
        }
        .practice-features .material-symbols-outlined {
          color: var(--md-success, #28a745);
          font-size: 16px;
          margin-right: 8px;
          transition: color 0.3s;
        }
      </style>
      HTML
    end
  end
end 