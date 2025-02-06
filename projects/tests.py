import time
import unittest

from colorama import Fore, Style, init
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comment, Contributor, Issue, Project

init()
User = get_user_model()

def print_test_header(test_name):
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"Test: {test_name}")
    print(f"{'=' * 50}{Style.RESET_ALL}")

def print_step(message):
    print(f"{Fore.WHITE}➤ {message}{Style.RESET_ALL}")

def print_result(success, message=""):
    if success:
        print(f"{Fore.GREEN}✅ Test réussi - {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Test échoué - {message}{Style.RESET_ALL}")
        

class UserTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"\n{Fore.CYAN}🚀 DÉMARRAGE DES TESTS UTILISATEURS{Style.RESET_ALL}\n")

    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.start_time = time.time()
        test_name = self._testMethodName
        print_test_header(test_name)
        print(f"{Fore.YELLOW}⏳ Démarrage du test...{Style.RESET_ALL}")

    def test_01_user_creation_success(self):
        """Test la création d'un utilisateur avec des données valides"""
        try:
            print_step("Tentative de création d'un utilisateur avec âge valide")
            data = {
                "username": "test_user",
                "password": "Password123!",
                "date_of_birth": "1990-01-01",
                "can_be_contacted": True,
                "can_data_be_shared": True
            }
            response = self.client.post('/api/users/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print_result(True, "L'utilisateur a été créé avec succès")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_02_user_creation_underage(self):
        """Test la création d'un utilisateur mineur (doit échouer)"""
        try:
            print_step("Tentative de création d'un utilisateur avec âge invalide")
            data = {
                "username": "young_user",
                "password": "Password123!",
                "date_of_birth": "2015-01-01",
                "can_be_contacted": True,
                "can_data_be_shared": True
            }
            response = self.client.post('/api/users/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print_result(True, "La création d'un utilisateur mineur a été refusée comme prévu")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_03_user_update_own_profile(self):
        """Test la modification de son propre profil"""
        try:
            # Création d'un utilisateur
            user = User.objects.create_user(
                username='update_user',
                password='Password123!',
                date_of_birth='1990-01-01'
            )
            self.client.force_authenticate(user=user)
            
            print_step("Tentative de modification de son propre profil")
            data = {
                "can_be_contacted": True,
                "can_data_be_shared": True
            }
            response = self.client.patch(f'/api/users/{user.id}/', data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print_result(True, "L'utilisateur peut modifier son propre profil")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_04_user_update_other_profile(self):
        """Test la modification du profil d'un autre utilisateur (doit échouer)"""
        try:
            # Création de deux utilisateurs
            user1 = User.objects.create_user(
                username='user1',
                password='Password123!',
                date_of_birth='1990-01-01'
            )
            user2 = User.objects.create_user(
                username='user2',
                password='Password123!',
                date_of_birth='1990-01-01'
            )
            self.client.force_authenticate(user=user1)
            
            print_step("Tentative de modification du profil d'un autre utilisateur")
            data = {
                "can_be_contacted": True
            }
            response = self.client.patch(f'/api/users/{user2.id}/', data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "La modification du profil d'un autre utilisateur a été refusée")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_05_user_delete_own_profile(self):
        """Test la suppression de son propre profil"""
        try:
            user = User.objects.create_user(
                username='delete_user',
                password='Password123!',
                date_of_birth='1990-01-01'
            )
            self.client.force_authenticate(user=user)
            
            print_step("Tentative de suppression de son propre profil")
            response = self.client.delete(f'/api/users/{user.id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            print_result(True, "L'utilisateur peut supprimer son propre profil")
        except AssertionError as e:
            print_result(False, str(e))
            raise
        
class ProjectTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"\n{Fore.CYAN}🚀 DÉMARRAGE DES TESTS PROJETS{Style.RESET_ALL}\n")

    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.start_time = time.time()
        test_name = self._testMethodName
        print_test_header(test_name)
        print(f"{Fore.YELLOW}⏳ Démarrage du test...{Style.RESET_ALL}")

        # Création des utilisateurs de test
        print_step("Création des utilisateurs de test")
        self.user1 = User.objects.create_user(
            username='project_creator',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.user2 = User.objects.create_user(
            username='project_contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.user3 = User.objects.create_user(
            username='non_contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )

    def test_01_project_creation_authenticated(self):
        """Test la création d'un projet par un utilisateur authentifié"""
        try:
            self.client.force_authenticate(user=self.user1)
            print_step("Tentative de création d'un projet")
            data = {
                "title": "Nouveau Projet",
                "description": "Description du projet",
                "type": "back-end"
            }
            response = self.client.post('/api/projects/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print_result(True, "Le projet a été créé avec succès")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_02_project_creation_unauthenticated(self):
        """Test la création d'un projet sans authentification"""
        try:
            print_step("Tentative de création d'un projet sans authentification")
            data = {
                "title": "Projet Non Autorisé",
                "description": "Description",
                "type": "back-end"
            }
            response = self.client.post('/api/projects/', data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            print_result(True, "La création sans authentification a été refusée")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_03_project_update_author(self):
        """Test la modification d'un projet par son auteur"""
        try:
            # Création du projet
            self.client.force_authenticate(user=self.user1)
            project_data = {
                "title": "Projet Test",
                "description": "Description",
                "type": "back-end"
            }
            project_response = self.client.post('/api/projects/', project_data)
            project_id = project_response.data['id']

            print_step("Tentative de modification du projet par l'auteur")
            update_data = {"title": "Projet Modifié"}
            response = self.client.patch(f'/api/projects/{project_id}/', update_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print_result(True, "L'auteur peut modifier son projet")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_04_project_update_contributor(self):
        """Test la modification d'un projet par un contributeur"""
        try:
            # Création du projet
            self.client.force_authenticate(user=self.user1)
            project_data = {
                "title": "Projet Test",
                "description": "Description",
                "type": "back-end"
            }
            project_response = self.client.post('/api/projects/', project_data)
            project_id = project_response.data['id']

            # Ajout du contributeur
            Contributor.objects.create(user=self.user2, project_id=project_id)

            # Tentative de modification par le contributeur
            self.client.force_authenticate(user=self.user2)
            print_step("Tentative de modification du projet par un contributeur")
            update_data = {"title": "Modification Non Autorisée"}
            response = self.client.patch(f'/api/projects/{project_id}/', update_data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Le contributeur ne peut pas modifier le projet")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_05_project_delete_author(self):
        """Test la suppression d'un projet par son auteur"""
        try:
            # Création du projet
            self.client.force_authenticate(user=self.user1)
            project_data = {
                "title": "Projet à Supprimer",
                "description": "Description",
                "type": "back-end"
            }
            project_response = self.client.post('/api/projects/', project_data)
            project_id = project_response.data['id']

            print_step("Tentative de suppression du projet par l'auteur")
            response = self.client.delete(f'/api/projects/{project_id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            print_result(True, "L'auteur peut supprimer son projet")
        except AssertionError as e:
            print_result(False, str(e))
            raise
        
class ContributorTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"\n{Fore.CYAN}🚀 DÉMARRAGE DES TESTS CONTRIBUTEURS{Style.RESET_ALL}\n")

    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.start_time = time.time()
        test_name = self._testMethodName
        print_test_header(test_name)
        print(f"{Fore.YELLOW}⏳ Démarrage du test...{Style.RESET_ALL}")

        # Création des utilisateurs de test
        print_step("Création des utilisateurs de test")
        self.project_author = User.objects.create_user(
            username='project_author',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.contributor = User.objects.create_user(
            username='contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.new_user = User.objects.create_user(
            username='new_user',
            password='Password123!',
            date_of_birth='1990-01-01'
        )

        # Création du projet test
        print_step("Création du projet test")
        self.client.force_authenticate(user=self.project_author)
        project_data = {
            "title": "Projet Test Contributeurs",
            "description": "Description",
            "type": "back-end"
        }
        response = self.client.post('/api/projects/', project_data)
        self.project = Project.objects.get(id=response.data['id'])

    def test_01_add_contributor_by_author(self):
        """Test l'ajout d'un contributeur par l'auteur du projet"""
        try:
            print_step("Tentative d'ajout d'un contributeur par l'auteur")
            self.client.force_authenticate(user=self.project_author)
            data = {"user": self.contributor.id}
            response = self.client.post(f'/api/projects/{self.project.id}/contributors/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print_result(True, "L'auteur peut ajouter un contributeur")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_02_add_contributor_by_contributor(self):
        """Test l'ajout d'un contributeur par un contributeur existant"""
        try:
            # Ajout du premier contributeur
            Contributor.objects.create(user=self.contributor, project=self.project)
            
            print_step("Tentative d'ajout d'un contributeur par un autre contributeur")
            self.client.force_authenticate(user=self.contributor)
            data = {"user": self.new_user.id}
            response = self.client.post(f'/api/projects/{self.project.id}/contributors/', data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Le contributeur ne peut pas ajouter d'autres contributeurs")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_03_remove_contributor_by_author(self):
        """Test la suppression d'un contributeur par l'auteur"""
        try:
            # Ajout d'un contributeur
            contributor = Contributor.objects.create(user=self.contributor, project=self.project)
            
            print_step("Tentative de suppression d'un contributeur par l'auteur")
            self.client.force_authenticate(user=self.project_author)
            response = self.client.delete(f'/api/projects/{self.project.id}/contributors/{contributor.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print_result(True, "L'auteur peut supprimer un contributeur")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_04_remove_contributor_by_contributor(self):
        """Test la suppression d'un contributeur par un autre contributeur"""
        try:
            # Ajout de deux contributeurs
            contributor1 = Contributor.objects.create(user=self.contributor, project=self.project)
            Contributor.objects.create(user=self.new_user, project=self.project)
            
            print_step("Tentative de suppression d'un contributeur par un autre contributeur")
            self.client.force_authenticate(user=self.new_user)
            response = self.client.delete(f'/api/projects/{self.project.id}/contributors/{contributor1.id}/')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Un contributeur ne peut pas supprimer d'autres contributeurs")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_05_remove_author_as_contributor(self):
        """Test la tentative de suppression de l'auteur comme contributeur"""
        try:
            # Récupérer le contributeur de l'auteur
            author_contributor = Contributor.objects.get(user=self.project_author, project=self.project)
            
            print_step("Tentative de suppression de l'auteur comme contributeur")
            self.client.force_authenticate(user=self.project_author)
            response = self.client.delete(f'/api/projects/{self.project.id}/contributors/{author_contributor.id}/')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print_result(True, "Impossible de supprimer l'auteur des contributeurs")
        except AssertionError as e:
            print_result(False, str(e))
            raise
        
class IssueTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"\n{Fore.CYAN}🚀 DÉMARRAGE DES TESTS ISSUES{Style.RESET_ALL}\n")

    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.start_time = time.time()
        test_name = self._testMethodName
        print_test_header(test_name)
        print(f"{Fore.YELLOW}⏳ Démarrage du test...{Style.RESET_ALL}")

        # Création des utilisateurs de test
        print_step("Création des utilisateurs de test")
        self.project_author = User.objects.create_user(
            username='project_author',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.contributor = User.objects.create_user(
            username='contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.non_contributor = User.objects.create_user(
            username='non_contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )

        # Création du projet test
        print_step("Création du projet test")
        self.client.force_authenticate(user=self.project_author)
        project_data = {
            "title": "Projet Test Issues",
            "description": "Description",
            "type": "back-end"
        }
        response = self.client.post('/api/projects/', project_data)
        self.project = Project.objects.get(id=response.data['id'])

        # Ajout du contributeur
        Contributor.objects.create(user=self.contributor, project=self.project)

    def test_01_create_issue_by_contributor(self):
        """Test la création d'une issue par un contributeur"""
        try:
            print_step("Tentative de création d'une issue par un contributeur")
            self.client.force_authenticate(user=self.contributor)
            data = {
                "title": "Bug Test",
                "description": "Description du bug",
                "priority": "HIGH",
                "tag": "BUG",
                "status": "To Do"
            }
            response = self.client.post(f'/api/projects/{self.project.id}/issues/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print_result(True, "Le contributeur peut créer une issue")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_02_create_issue_by_non_contributor(self):
        """Test la création d'une issue par un non-contributeur"""
        try:
            print_step("Tentative de création d'une issue par un non-contributeur")
            self.client.force_authenticate(user=self.non_contributor)
            data = {
                "title": "Bug Test",
                "description": "Description du bug",
                "priority": "HIGH",
                "tag": "BUG",
                "status": "To Do"
            }
            response = self.client.post(f'/api/projects/{self.project.id}/issues/', data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Le non-contributeur ne peut pas créer d'issue")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_03_update_own_issue(self):
        """Test la modification d'une issue par son auteur"""
        try:
            # Création d'une issue
            self.client.force_authenticate(user=self.contributor)
            issue_data = {
                "title": "Issue Test",
                "description": "Description",
                "priority": "HIGH",
                "tag": "BUG",
                "status": "To Do"
            }
            create_response = self.client.post(f'/api/projects/{self.project.id}/issues/', issue_data)
            issue_id = create_response.data['id']

            print_step("Tentative de modification de sa propre issue")
            update_data = {"status": "In Progress"}
            response = self.client.patch(f'/api/projects/{self.project.id}/issues/{issue_id}/', update_data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print_result(True, "L'auteur peut modifier sa propre issue")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_04_update_other_issue(self):
        """Test la modification d'une issue par un autre contributeur"""
        try:
            # Création d'une issue par le contributeur
            self.client.force_authenticate(user=self.contributor)
            issue_data = {
                "title": "Issue Test",
                "description": "Description",
                "priority": "HIGH",
                "tag": "BUG",
                "status": "To Do"
            }
            create_response = self.client.post(f'/api/projects/{self.project.id}/issues/', issue_data)
            issue_id = create_response.data['id']

            # Tentative de modification par l'auteur du projet
            print_step("Tentative de modification d'une issue par un autre contributeur")
            self.client.force_authenticate(user=self.project_author)
            update_data = {"status": "In Progress"}
            response = self.client.patch(f'/api/projects/{self.project.id}/issues/{issue_id}/', update_data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Un autre contributeur ne peut pas modifier l'issue")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_05_delete_own_issue(self):
        """Test la suppression d'une issue par son auteur"""
        try:
            # Création d'une issue
            self.client.force_authenticate(user=self.contributor)
            issue_data = {
                "title": "Issue à supprimer",
                "description": "Description",
                "priority": "HIGH",
                "tag": "BUG",
                "status": "To Do"
            }
            create_response = self.client.post(f'/api/projects/{self.project.id}/issues/', issue_data)
            issue_id = create_response.data['id']

            print_step("Tentative de suppression de sa propre issue")
            response = self.client.delete(f'/api/projects/{self.project.id}/issues/{issue_id}/')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            print_result(True, "L'auteur peut supprimer sa propre issue")
        except AssertionError as e:
            print_result(False, str(e))
            raise
        
class CommentTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"\n{Fore.CYAN}🚀 DÉMARRAGE DES TESTS COMMENTAIRES{Style.RESET_ALL}\n")

    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.start_time = time.time()
        test_name = self._testMethodName
        print_test_header(test_name)
        print(f"{Fore.YELLOW}⏳ Démarrage du test...{Style.RESET_ALL}")

        # Création des utilisateurs de test
        print_step("Création des utilisateurs de test")
        self.project_author = User.objects.create_user(
            username='project_author',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.contributor = User.objects.create_user(
            username='contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )
        self.non_contributor = User.objects.create_user(
            username='non_contributor',
            password='Password123!',
            date_of_birth='1990-01-01'
        )

        # Création du projet test
        print_step("Création du projet test")
        self.client.force_authenticate(user=self.project_author)
        project_data = {
            "title": "Projet Test Commentaires",
            "description": "Description",
            "type": "back-end"
        }
        response = self.client.post('/api/projects/', project_data)
        self.project = Project.objects.get(id=response.data['id'])

        # Ajout du contributeur
        Contributor.objects.create(user=self.contributor, project=self.project)

        # Création d'une issue pour les tests
        print_step("Création d'une issue pour les tests")
        issue_data = {
            "title": "Issue Test",
            "description": "Description",
            "priority": "HIGH",
            "tag": "BUG",
            "status": "To Do"
        }
        response = self.client.post(f'/api/projects/{self.project.id}/issues/', issue_data)
        self.issue = Issue.objects.get(id=response.data['id'])

    def test_01_create_comment_by_contributor(self):
        """Test la création d'un commentaire par un contributeur"""
        try:
            print_step("Tentative de création d'un commentaire par un contributeur")
            self.client.force_authenticate(user=self.contributor)
            data = {
                "description": "Commentaire de test"
            }
            response = self.client.post(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/',
                data
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print_result(True, "Le contributeur peut créer un commentaire")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_02_create_comment_by_non_contributor(self):
        """Test la création d'un commentaire par un non-contributeur"""
        try:
            print_step("Tentative de création d'un commentaire par un non-contributeur")
            self.client.force_authenticate(user=self.non_contributor)
            data = {
                "description": "Commentaire non autorisé"
            }
            response = self.client.post(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/',
                data
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Le non-contributeur ne peut pas créer de commentaire")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_03_update_own_comment(self):
        """Test la modification d'un commentaire par son auteur"""
        try:
            # Création d'un commentaire
            self.client.force_authenticate(user=self.contributor)
            comment_data = {
                "description": "Commentaire initial"
            }
            create_response = self.client.post(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/',
                comment_data
            )
            comment_id = create_response.data['id']

            print_step("Tentative de modification de son propre commentaire")
            update_data = {
                "description": "Commentaire modifié"
            }
            response = self.client.put(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment_id}/',
                update_data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            print_result(True, "L'auteur peut modifier son propre commentaire")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_04_update_other_comment(self):
        """Test la modification d'un commentaire par un autre contributeur"""
        try:
            # Création d'un commentaire par le contributeur
            self.client.force_authenticate(user=self.contributor)
            comment_data = {
                "description": "Commentaire initial"
            }
            create_response = self.client.post(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/',
                comment_data
            )
            comment_id = create_response.data['id']

            # Tentative de modification par l'auteur du projet
            print_step("Tentative de modification d'un commentaire par un autre contributeur")
            self.client.force_authenticate(user=self.project_author)
            update_data = {
                "description": "Modification non autorisée"
            }
            response = self.client.put(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment_id}/',
                update_data
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            print_result(True, "Un autre contributeur ne peut pas modifier le commentaire")
        except AssertionError as e:
            print_result(False, str(e))
            raise

    def test_05_delete_own_comment(self):
        """Test la suppression d'un commentaire par son auteur"""
        try:
            # Création d'un commentaire
            self.client.force_authenticate(user=self.contributor)
            comment_data = {
                "description": "Commentaire à supprimer"
            }
            create_response = self.client.post(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/',
                comment_data
            )
            comment_id = create_response.data['id']

            print_step("Tentative de suppression de son propre commentaire")
            response = self.client.delete(
                f'/api/projects/{self.project.id}/issues/{self.issue.id}/comments/{comment_id}/'
            )
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            print_result(True, "L'auteur peut supprimer son propre commentaire")
        except AssertionError as e:
            print_result(False, str(e))
            raise
        
def print_test_summary(success_count, total_count):
    print(f"\n{Fore.CYAN}{'=' * 50}")
    print(f"📊 RÉSUMÉ DES TESTS")
    print(f"{'=' * 50}")
    print(f"Tests réussis: {Fore.GREEN}{success_count}{Style.RESET_ALL}")
    print(f"Tests totaux: {total_count}")
    success_rate = (success_count / total_count) * 100
    color = Fore.GREEN if success_rate == 100 else Fore.YELLOW if success_rate >= 80 else Fore.RED
    print(f"Taux de réussite: {color}{success_rate:.1f}%{Style.RESET_ALL}")
    print(f"{'=' * 50}{Style.RESET_ALL}\n")

class TestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        success_count = result.testsRun - len(result.failures) - len(result.errors)
        print_test_summary(success_count, result.testsRun)
        return result

if __name__ == '__main__':
    print(f"\n{Fore.CYAN}🚀 DÉMARRAGE DE LA SUITE DE TESTS COMPLÈTE{Style.RESET_ALL}\n")
    unittest.main(testRunner=TestRunner)