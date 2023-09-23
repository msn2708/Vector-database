def get_paragraphs(content):
  paragraphs = content.split('\n')
  for para in paragraphs:
    para.replace('\n',' ')
    para.replace('\t', ' ')
    para = ''.join(para.split())

    para.strip()
    if len(para) == 0:
      #remove para from paragraphs
      paragraphs.remove(para)
  return paragraphs