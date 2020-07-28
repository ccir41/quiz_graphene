import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Category, Question, Option

# Create a GraphQL type

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class OptionType(DjangoObjectType):
    class Meta:
        model = Option


# Create a Query Type

class Query(ObjectType):
    category = graphene.Field(CategoryType, id=graphene.Int())
    question = graphene.Field(QuestionType, id=graphene.Int())
    option = graphene.Field(OptionType, id=graphene.Int())

    categories = graphene.List(CategoryType)
    questions = graphene.List(QuestionType, categoryId=graphene.Int())
    options = graphene.List(OptionType, questionId=graphene.Int())

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Category.objects.get(pk=id)
        return None
    
    def resolve_question(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Question.objects.get(pk=id)
        return None
    
    def resolve_option(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Option.objects.get(pk=id)
        return None
    
    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_questions(self, info, **kwargs):
        categoryId = kwargs.get('categoryId')
        if categoryId is not None:
            return Question.objects.filter(category_id=categoryId)
        return Question.objects.all()
    
    def resolve_options(self, info, **kwargs):
        questionId = kwargs.get('questionId')
        if questionId is not None:
            return Option.objects.filter(question_id=questionId)
        return Question.objects.all()


# Create a Input Object Type

class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class OptionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    isAnswer = graphene.Boolean()
    question = graphene.Int()


class QuestionInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    category = graphene.Int()
    options = graphene.List(OptionInput)


# Create Mutations

class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)
    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category = Category.objects.create(**input)
        return CreateCategory(ok=ok, category=category)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CategoryInput(required=True)
    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        category_instance = Category.objects.get(pk=id)
        if category_instance:
            ok = True
            category_instance.name = input.name
            category_instance.save()
            return UpdateCategory(ok=ok, category=category_instance)
        return UpdateCategory(ok=ok, category=None)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        ok = False
        category_instance = Category.objects.get(pk=id)
        if category_instance:
            ok = True
            category_instance.delete()
            return DeleteCategory(ok=ok)
        return DeleteCategory(ok=ok)


class CreateQuestion(graphene.Mutation):
    class Arguments:
        input = QuestionInput(required=True)
    ok = graphene.Boolean()
    question = graphene.Field(QuestionType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        question = Question.objects.create(
            name = input.name,
            category_id = input.category   
        )
        for opt in input.options:
            opt['question'] = question
            Option.objects.create(**opt)
        
        return CreateQuestion(ok=ok, question=question)
    

class UpdateQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = QuestionInput(required=True)
    ok = graphene.Boolean()
    question = graphene.Field(QuestionType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        question_instance = Question.objects.get(pk=id)
        if question_instance:
            ok = True
            question_instance.name = input.name
            question_instance.category_id = input.category
            for opt in input.options:
                Option.objects.filter(id=opt.id).update(name=opt.name, isAnswer=opt.isAnswer)
            question_instance.save()
            return UpdateQuestion(ok=ok, question=question_instance)
        return UpdateQuestion(ok=ok, question=None)


class DeleteQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        ok = False
        question_instance = Question.objects.get(pk=id)
        if question_instance:
            ok = True
            question_instance.delete()
            return DeleteQuestion(ok=ok)
        return DeleteQuestion(ok=ok)


class CreateOption(graphene.Mutation):
    class Arguments:
        input = OptionInput(required=True)
    ok = graphene.Boolean()
    option = graphene.Field(OptionType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        option = Option.objects.create(
            name = input.name,
            isAnswer = input.isAnswer,
            question_id = input.question
        )
        return CreateOption(ok=ok, option=option)


class UpdateOption(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = OptionInput(required=True)
    ok = graphene.Boolean()
    option = graphene.Field(OptionType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        option_instance = Option.objects.get(pk=id)
        if option_instance:
            ok = True
            option_instance.name = input.name
            option_instance.question_id = input.question
            option_instance.isAnswer = input.isAnswer
            option_instance.save()
            return UpdateOption(ok=ok, option=option_instance)
        return UpdateOption(ok=ok, option=None)


class DeleteOption(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        ok = False
        option_instance = Option.objects.get(pk=id)
        if option_instance:
            ok = True
            option_instance.delete()
            return DeleteQuestion(ok=ok)
        return DeleteQuestion(ok=ok)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()
    
    create_option = CreateOption.Field()
    update_option = UpdateOption.Field()
    delete_option = DeleteOption.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)
