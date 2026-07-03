import frappe

@frappe.whitelist(allow_guest=True)
def get_blogs():

    blogs = frappe.get_all(
        "Blogs",
        fields=[
            "name",
            "creation",
            "blog_date",
            "header_image",
            "thumbnail_image",
            "description_heading_1",
            "description_1",
            "description_heading_2",
            "description_2",
            "description_heading_3",
            "description_3",
            "description_heading_4",
            "description_4",
            "sub_description_heading_1",
            "sub_description_heading_2",
            "sub_description_heading_3",
            "sub_description_heading_4",
            "custom_html",
            "url",
            "meta_title",
            "meta_description"
        ],
        order_by="creation desc"
    )

    for blog in blogs:
        if blog.get("header_image"):
            blog["header_image"] = frappe.utils.get_url(blog["header_image"])

        if blog.get("thumbnail_image"):
            blog["thumbnail_image"] = frappe.utils.get_url(blog["thumbnail_image"])

    return blogs


@frappe.whitelist(allow_guest=True)
def get_blog(blog_name=None, url=None):

    blog = None

    if url:

        blogs = frappe.get_all(
            "Blogs",
            filters={"url": url},
            fields=["name"],
            limit=1
        )

        if not blogs:
            return {}

        blog = frappe.get_doc("Blogs", blogs[0].name)

    elif blog_name:

        blog = frappe.get_doc("Blogs", blog_name)

    else:
        return {}

    if blog.header_image:
        blog.header_image = frappe.utils.get_url(blog.header_image)

    if blog.thumbnail_image:
        blog.thumbnail_image = frappe.utils.get_url(blog.thumbnail_image)

    return {
        "name": blog.name,
        "creation": blog.creation,
        "blog_date": blog.blog_date,
        "header_image": blog.header_image,
        "thumbnail_image": blog.thumbnail_image,
        "description_heading_1": blog.description_heading_1,
        "description_1": blog.description_1,
        "description_heading_2": blog.description_heading_2,
        "description_2": blog.description_2,
        "description_heading_3": blog.description_heading_3,
        "description_3": blog.description_3,
        "description_heading_4": blog.description_heading_4,
        "description_4": blog.description_4,
        "sub_description_heading_1": blog.sub_description_heading_1,
        "sub_description_heading_2": blog.sub_description_heading_2,
        "sub_description_heading_3": blog.sub_description_heading_3,
        "sub_description_heading_4": blog.sub_description_heading_4,
        "custom_html": blog.custom_html,
        "url": blog.url,
        "meta_title": blog.meta_title,
        "meta_description": blog.meta_description
    }