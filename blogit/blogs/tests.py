from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import Client, TestCase

from .models import Blogs, Likes
from .serializers import AboutUserSerializer, GetBlogsSerializer, LikeSerializer


class BlogsTestModels(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test", email="test@mail.com")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def test_blogs_model(self) -> None:
        ## checking initially if there are any blogs present
        self.assertEqual(Blogs.objects.all().count(), 0)

        ## creating a new blog
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=self.user,
            tags="some random tags",
        )

        ## making sure that our blog is inserted
        self.assertEqual(Blogs.objects.all().count(), 1)
        self.assertIsNotNone(Blogs.objects.get(id=blog.pk))

    def test_likes_model(self) -> None:
        ## checking initially if there are any likes present
        self.assertEqual(Likes.objects.all().count(), 0)

        ## creating a new blog as before creating a like it will be required
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=self.user,
            tags="some random tags",
        )
        likes = Likes.objects.create(liked_by=self.user, blog=blog)

        ## making sure that our like is inserted
        self.assertEqual(Likes.objects.all().count(), 1)
        self.assertIsNotNone(Likes.objects.get(id=likes.pk))

        ## if we donot pass blog while creating likes then it will throw Error
        expected_constraint = "NOT NULL constraint failed: blogs_likes.blog_id"
        with self.assertRaisesRegex(IntegrityError, expected_constraint):
            Likes.objects.create(liked_by=self.user)


class BlogsTestSerializers(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test", email="test@mail.com")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def test_about_user_serializer(self) -> None:
        ## serializer used to return the user model information
        serializer = AboutUserSerializer(instance=self.user)
        serializer_data = serializer.data
        self.assertEqual(
            list(serializer_data.keys()),
            ["username", "email", "first_name", "last_name", "blogs"],
        )

        ## testing the method field as well in which we are returning the blogs information by the user
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=self.user,
            tags="some random tags",
        )

        serializer = AboutUserSerializer(instance=self.user)
        serializer_data = serializer.data
        ## testing if the serializer is created with the blog
        self.assertEqual(list(serializer_data["blogs"]), [blog.title])

    def test_get_blog_serializer(self) -> None:
        ## serializer used to return the Blogs information
        # so firstly creating a blog
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=self.user,
            tags="some random tags",
        )

        serializer = GetBlogsSerializer(instance=blog)
        serializer_data = serializer.data

        self.assertEqual(
            list(serializer_data.keys()),
            ["id", "title", "created_at", "author", "author_id", "content", "likes"],
        )
        self.assertEqual(serializer_data.get("id"), blog.id)
        self.assertEqual(serializer_data.get("title"), blog.title)
        self.assertEqual(serializer_data.get("likes"), 0)

        ## now creating likes
        Likes.objects.create(liked_by=self.user, blog=blog)

        serializer = GetBlogsSerializer(instance=blog)
        serializer_data = serializer.data

        self.assertEqual(serializer_data.get("likes"), 1)

        ## creating a new user which will also likes our test blog
        new_user = User.objects.create(username="test1", email="test1@mail.com")
        Likes.objects.create(liked_by=new_user, blog=blog)

        serializer = GetBlogsSerializer(instance=blog)
        serializer_data = serializer.data

        ## total likes would be 2 --> self.user + new_user
        self.assertEqual(serializer_data.get("likes"), 2)

    def test_update_blogs_serializer(self) -> None:
        ## serializer used to return the Blogs information
        # so firstly creating a blog
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=self.user,
            tags="some random tags",
        )

        serializer = GetBlogsSerializer(instance=blog)
        serializer_data = serializer.data

        self.assertEqual(
            list(serializer_data.keys()),
            ["id", "title", "created_at", "author", "author_id", "content", "likes"],
        )
        self.assertEqual(serializer_data.get("id"), blog.id)
        self.assertEqual(serializer_data.get("title"), blog.title)
        self.assertEqual(serializer_data.get("likes"), 0)

        ## now updating title
        updated_value = {"title": "new title"}

        serializer = GetBlogsSerializer(instance=blog)
        instance = serializer.update(blog, updated_value)

        updated_data = serializer.data

        ## check if our title has been updated or not
        self.assertEqual(updated_data.get("title"), updated_value["title"])

    def test_like_serializer(self) -> None:
        ## creating likes for testing our serializer
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=self.user,
            tags="some random tags",
        )
        likes = Likes.objects.create(liked_by=self.user, blog=blog)

        serializer = LikeSerializer(instance=likes)
        serializer_data = serializer.data

        ## checking the results
        self.assertEqual(list(serializer_data.keys()), ["id"])
        self.assertEqual(serializer_data.get("id"), likes.id)


class BlogsTestViews(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test", email="test@mail.com")
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client = Client()

    def test_get_user_information_view(self) -> None:
        user = self.user
        self.client.force_login(user)

        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=user,
            tags="some random tags",
        )

        response = self.client.get("/blogs/users")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["username"], user.username)
        self.assertEqual(data[0]["email"], user.email)
        self.assertEqual(len(data[0]["blogs"]), 1)
        self.assertIn(blog.title, data[0]["blogs"])

        ## creating new user
        User.objects.create(username="test1", email="test1@mail.com")

        ## checking if the newly created user is coming from the api
        response = self.client.get("/blogs/users")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_blog_list(self) -> None:
        user = self.user
        self.client.force_login(user)

        response = self.client.get("/blogs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=user,
            tags="some random tags",
        )

        response = self.client.get("/blogs/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["id"], blog.id)
        self.assertEqual(response.json()[0]["title"], blog.title)
        self.assertEqual(response.json()[0]["author"], blog.posted_by.username)

    def test_blog_update(self) -> None:
        user = self.user
        self.client.force_login(user)

        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=user,
            tags="some random tags",
        )

        pk = blog.id

        params = {"title": "new title", "content": "updated content"}
        response = self.client.put(
            f"/blogs/{pk}", data=params, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], pk)
        self.assertEqual(response.json()["title"], params["title"])
        self.assertEqual(response.json()["content"], params["content"])

        ## creating new user
        new_user = User.objects.create(username="test1", email="test1@mail.com")
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=new_user,
            tags="some random tags",
        )

        pk = blog.id

        response = self.client.put(
            f"/blogs/{pk}", data=params, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ["You cannot update other person's post !!"])

    def test_likes_created(self) -> None:
        user = self.user
        self.client.force_login(user)

        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=user,
            tags="some random tags",
        )

        pk = blog.id

        response = self.client.post(f"/blogs/{pk}/like")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

        ## liking the same post again
        response = self.client.post(f"/blogs/{pk}/like")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ["You have already voted for this post !!"])

        ## deleting the like
        response = self.client.delete(f"/blogs/{pk}/like")
        self.assertEqual(response.status_code, 204)

        ## deleting the like again
        response = self.client.delete(f"/blogs/{pk}/like")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ["There is nothing to delete here .."])

    def test_blog_destroy(self) -> None:
        user = self.user
        self.client.force_login(user)

        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=user,
            tags="some random tags",
        )

        pk = blog.id

        ## deleting the blog
        response = self.client.delete(f"/blogs/{pk}/delete")
        self.assertEqual(response.status_code, 204)

        ## creating new user
        new_user = User.objects.create(username="test1", email="test1@mail.com")
        blog = Blogs.objects.create(
            title="test title",
            content="test-content",
            posted_by=new_user,
            tags="some random tags",
        )

        pk = blog.id

        ## deleting the blog of other person
        response = self.client.delete(f"/blogs/{pk}/delete")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), ["You cannot delete other person's blog !!"])
