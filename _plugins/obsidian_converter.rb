module Jekyll
    class ObsidianLinkConverter < Converter
      safe true
      priority :low
  
      def matches(ext)
        ext =~ /^\.md$/i
      end
  
      def output_ext(ext)
        ".html"
      end
  
      def convert(content)
        content = convert_links(content)
        content
      end
  
      private
  
      def convert_links(content)
        # 패턴을 찾아서 링크를 변환
        content.gsub(/\[([^\]]+)\]\(([^)]+)\)/) do
          link_text = $1
          link_url = $2
  
          if link_url.include?("#")
            # 헤딩을 참조하는 경우
            link_url = convert_heading_link(link_url)
          else
            # 일반 문서 링크인 경우
            link_url = convert_document_link(link_url)
          end
  
          "[#{link_text}](#{link_url})"
        end
      end
  
      def convert_document_link(link_url)
        # yyyy-mm-dd- 형식을 제거
        link_url = link_url.gsub(/\d{4}-\d{2}-\d{2}-/, '')
  
        # .md 확장자를 제거
        link_url = link_url.gsub(/\.md$/, '')
  
        # baseurl 앞에 붙이기
        link_url = "{{ site.baseurl }}/#{link_url}"
  
        link_url
      end
  
      def convert_heading_link(link_url)
        # 문서 링크와 헤딩 부분을 분리
        document_part, heading_part = link_url.split("#", 2)
  
        # 문서 링크 부분을 처리
        document_part = convert_document_link(document_part) unless document_part.empty?
  
        # heading 부분을 변환
        heading_part = convert_heading(heading_part) if heading_part
  
        # 링크를 결합
        "#{document_part}##{heading_part}"
      end
  
      def convert_heading(heading)
        # %20을 -로 변환
        heading = heading.gsub("%20", "-")
  
        # 특수문자 제거
        heading = heading.gsub(/[^a-zA-Z0-9\-]/, '')
  
        heading
      end
    end
  end
  