import PyPDF2

# 将第一个 PDF 的第一页顺时针旋转 90 度，另存为文件
with open("first.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    print(len(reader.pages))

    page = reader.pages[0]
    page.rotate(90)

    writer = PyPDF2.PdfWriter()
    writer.add_page(page)

    with open("rotated.pdf", "wb") as output:
        writer.write(output)

# # combine multiple PDFs into a single PDF 将两个原始 PDF 合并
merger = PyPDF2.PdfMerger()

for file_name in ["first.pdf", "second.pdf"]:
    merger.append(file_name)

merger.write("combined.pdf")
merger.close()
