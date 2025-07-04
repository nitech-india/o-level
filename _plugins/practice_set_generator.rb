module Jekyll
  class PracticeSetGenerator < Generator
    safe true

    def generate(site)
      # Find all practice data files (regular and comprehensive)
      practice_files = [
        'm1r5_practice', 'm2r5_practice', 'm3r5_practice', 'm4r5_practice',
        'm1r5_comprehensive', 'm2r5_comprehensive', 'm3r5_comprehensive', 'm4r5_comprehensive',
        'match_together_questions', 'multiple_answer_questions'
      ]
      
      practice_files.each do |file_key|
        next unless site.data.key?(file_key)
        
        data = site.data[file_key]
        next unless data.is_a?(Hash) && data.key?('sets')
        
        data['sets'].each do |set_info|
          # Extract module name for module-specific files
          module_name = nil
          is_comprehensive = false
          
          if file_key.match(/^(m\d)r(\d)/)
            module_match = file_key.match(/^(m\d)r(\d)/)
            module_name = "#{module_match[1].upcase}-R#{module_match[2]}"
            is_comprehensive = file_key.include?('comprehensive')
          else
            # For question type files like match_together_questions and multiple_answer_questions
            question_type = file_key.gsub('_questions', '').capitalize
            module_name = question_type
          end

          # --- Normalize questions ---
          if set_info['questions'].is_a?(Array)
            set_info['questions'] = set_info['questions'].map do |q|
              # Convert choices hash to array of {letter, text} for MCQ/multiple, but preserve array for match
              choices_arr = if q['type'] == 'match' && q['choices'].is_a?(Array)
                q['choices']
              elsif q['choices'].is_a?(Hash) && !q['choices'].empty?
                q['choices'].map { |letter, text| { 'letter' => letter, 'text' => text } }
              else
                []
              end

              # Ensure type and answer are normalized
              type = q['type']
              answer = q['answer']
              if type == 'match'
                # keep type as 'match'
              elsif type == 'multiple' || answer.is_a?(Array)
                type = 'multiple'
                answer = Array(answer)
              end

              # Merge all original fields, then override with normalized ones
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
          # --- End normalization ---

          # Create page directory path
          if file_key.match(/^m\d/)
            # For module-specific files
            if is_comprehensive
              page_dir = "practice-sets/#{file_key.gsub('_', '-')}-#{set_info['id']}"
            else
              page_dir = "practice-sets/#{file_key.gsub('_', '-')}-#{set_info['id']}"
            end
          else
            # For question type files
            page_dir = "practice-sets/#{file_key.gsub('_', '-')}-#{set_info['id']}"
          end
          
          # Create and add the page
          site.pages << PracticeSetPage.new(site, site.source, page_dir, set_info, module_name, is_comprehensive)
        end
      end
    end
  end

  class PracticeSetPage < Page
    def initialize(site, base, dir, practice_set, module_name, is_comprehensive = false)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      
      # Set page data
      self.data = {}
      self.data['layout'] = 'practice'
      
      # Set title based on whether it's comprehensive, module-specific, or question type
      if module_name.match(/^M\d-R\d$/)
        # Module-specific title
        if is_comprehensive
          self.data['title'] = "Module #{module_name} Comprehensive Practice Set ##{practice_set['id']}"
        else
          self.data['title'] = "Module #{module_name} Practice Set ##{practice_set['id']}"
        end
      else
        # Question type title
        self.data['title'] = "Practice Set ##{practice_set['id']}"
      end
      
      self.data['practice_set'] = practice_set
      self.data['is_comprehensive'] = is_comprehensive
      self.data['module_name'] = module_name
      
      # Set content
      self.content = generate_content(module_name, is_comprehensive, practice_set)
    end

    private

    def generate_content(module_name, is_comprehensive, practice_set)
      content = ""
      
      if is_comprehensive
        content += "<div class='comprehensive-banner'>"
        content += "<h2>📋 Comprehensive Practice Set</h2>"
        content += "<p>This is a full-length practice set simulating actual exam conditions.</p>"
        content += "<ul>"
        content += "<li><strong>Total Questions:</strong> #{practice_set['questions'].size}</li>"
        content += "<li><strong>Duration:</strong> #{practice_set['duration_minutes']} minutes</li>"
        content += "<li><strong>Total Marks:</strong> 100</li>"
        content += "</ul>"
        content += "</div>"
      elsif !module_name.match(/^M\d-R\d$/)
        # For question type practice sets
        content += "<div class='question-type-banner'>"
        content += "<h2>#{module_name} Questions</h2>"
        content += "<p>This practice set focuses on #{module_name.downcase} questions.</p>"
        content += "<ul>"
        content += "<li><strong>Total Questions:</strong> #{practice_set['questions'].size}</li>"
        content += "<li><strong>Duration:</strong> #{practice_set['duration_minutes']} minutes</li>"
        content += "</ul>"
        content += "</div>"
      end
      
      if module_name.match(/^M\d-R\d$/)
        content += "<p>This practice set contains questions for Module #{module_name}. "
      else
        content += "<p>This practice set contains #{module_name.downcase} questions. "
      end
      content += "Select your answer for each question to see immediate feedback.</p>\n"
      content += "<p>Questions are shown one per page. Use the navigation buttons to move between pages.</p>\n"
      
      if is_comprehensive
        content += "<div class='exam-tips'>"
        content += "<h3>💡 Exam Tips</h3>"
        content += "<ul>"
        content += "<li>Manage your time wisely - you have #{practice_set['duration_minutes']} minutes for #{practice_set['questions'].size} questions</li>"
        content += "<li>Read each question carefully before answering</li>"
        content += "<li>Don't spend too much time on any single question</li>"
        content += "<li>Review your answers if time permits</li>"
        content += "</ul>"
        content += "</div>"
      end
      
      content
    end
  end
end 