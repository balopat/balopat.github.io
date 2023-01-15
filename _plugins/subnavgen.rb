require "nokogiri"

class MySubnavGenerator < Jekyll::Generator
  def generate(site)
    parser = Jekyll::Converters::Markdown.new(site.config)

    site.posts.docs.each do |post|      
      post.read()
      doc = Nokogiri::HTML(parser.convert(post.content))
      post.data["subnav"] = []
      doc.css('h2').each do |heading|
        post.data["subnav"] << { "title" => heading.text, "url" => [post.url, heading['id']].join("#") }
      end
    
    end
  end
end