from django.test import TestCase
from django.core.validators import ValidationError


from .models import (CaseStudy,
                     Implementation,
                     Solution,
                     SolutionCategory,
                     SolutionInImplementation,
                     SolutionInImplementationGeometry,
                     SolutionInImplementationNote,
                     SolutionInImplementationQuantity,
                     SolutionQuantity,
                     SolutionRatioOneUnit,
                     Stakeholder,
                     StakeholderCategory,
                     Strategy,
                     Unit,
                     User,
                     UserInCasestudy,
                     )


class ModelTest(TestCase):

    fixtures = ['changes_fixture.json',]

    def test_string_representation(self):
        for Model in (CaseStudy,
                     Implementation,
                     Solution,
                     SolutionCategory,
                     SolutionRatioOneUnit,
                     Stakeholder,
                     StakeholderCategory,
                     Strategy,
                     Unit,
                     User,
                     ):

            model = Model(name="MyName")
            self.assertEqual(str(model),"MyName")

    def test_repr_of_solutions_in_implementations(self):
        """Test the solutions in implementations"""
        solution = Solution(name='Sol1')
        implementation = Implementation(name='Impl2')

        solution_in_impl = SolutionInImplementation(
            solution=solution,
            implementation=implementation)
        self.assertEqual(str(solution_in_impl), 'Sol1 in Impl2')

        model = SolutionInImplementationGeometry(
            sii=solution_in_impl,
            name='Altona',
            geom='LatLon',
        )
        target = 'location Altona at LatLon'
        self.assertEqual(str(model), target)

        model = SolutionInImplementationNote(
            sii=solution_in_impl,
            note='An important Note'
        )
        target = 'Note for Sol1 in Impl2:\nAn important Note'
        self.assertEqual(str(model), target)

        unit = Unit(name='tons')
        quantity = SolutionQuantity(name='bins', unit=unit)
        self.assertEqual(str(quantity), 'bins [tons]')

        model = SolutionInImplementationQuantity(
            sii=solution_in_impl,
            quantity=quantity,
            value=42,
        )
        self.assertEqual(str(model), '42 bins [tons]')


class ModelSolutionInImplementation(TestCase):

    def test01_new_solutionininplementation(self):
        """Test the new solution implementation"""
        user = User(name='user')
        user.save()
        casestudy = CaseStudy(name='city')
        casestudy.save()
        uic = UserInCasestudy(user=user, casestudy=casestudy)
        uic.save()

        solutioncategory = SolutionCategory(name='SolCat1', user=uic)
        solutioncategory.save()

        unit = Unit(name='yards')
        unit.save()


        implementation = Implementation(name='Impl2', user=uic)
        implementation.save()

        # create a solution that requires 2 quantities

        solution = Solution(name='Sol1', solution_category=solutioncategory,
                            user=uic)
        solution.save()

        solution_quantity1 = SolutionQuantity(solution=solution, name='q1', unit=unit)
        solution_quantity2 = SolutionQuantity(solution=solution, name='q2', unit=unit)
        solution_quantity1.save()
        solution_quantity2.save()

        # add solution to an implementation

        solution_in_impl = SolutionInImplementation(
            solution=solution,
            implementation=implementation)
        solution_in_impl.save()

        # check, if the SolutionInImplementationQuantity contains
        # now the 2 quantities

        solution_in_impl_quantities = SolutionInImplementationQuantity.\
            objects.filter(sii=solution_in_impl)
        solution_names = solution_in_impl_quantities.values_list(
            'quantity__name', flat=True)
        assert len(solution_names) == 2
        assert set(solution_names) == set(('q1', 'q2'))

        # create a solution that requires 3 quantities

        # add to the solution a third quantity
        solution_quantity3 = SolutionQuantity(solution=solution,
                                              name='q3', unit=unit)
        solution_quantity3.save()

        # check if the new quantity has been added to the related table
        solution_in_impl_quantities = SolutionInImplementationQuantity.\
            objects.filter(sii=solution_in_impl)
        solution_names = solution_in_impl_quantities.values_list(
            'quantity__name', flat=True)
        assert len(solution_names) == 3
        assert set(solution_names) == set(('q1', 'q2', 'q3'))

        # remove a solution quantity
        to_delete = SolutionQuantity.objects.filter(solution=solution,
                                                    name='q2')
        solution_id, deleted = to_delete.delete()
        # assert that 1 row in changes.SolutionInImplementationQuantity
        # are deleted
        assert deleted.get('changes.SolutionInImplementationQuantity') == 1

        # check the related SolutionInImplementationQuantity
        solution_in_impl_quantities = SolutionInImplementationQuantity.\
            objects.filter(sii=solution_in_impl)
        solution_names = solution_in_impl_quantities.values_list(
            'quantity__name', flat=True)
        assert len(solution_names) == 2
        assert set(solution_names) == set(('q1', 'q3'))

        # remove the solution_in_implementation
        sii_id, deleted = solution_in_impl.delete()
        # assert that 2 rows in changes.SolutionInImplementationQuantity
        # are deleted
        assert deleted.get('changes.SolutionInImplementationQuantity') == 2
        solution_in_impl_quantities = SolutionInImplementationQuantity.\
            objects.filter(sii=sii_id)
        assert not solution_in_impl_quantities

class UniqueNames(TestCase):

    def test01_unique_strategyname(self):
        """Test the unique strategy name"""
        user = User(name='user')
        user.save()
        casestudy1 = CaseStudy(name='city1')
        casestudy2 = CaseStudy(name='city2')
        casestudy1.save()
        casestudy2.save()
        uic1 = UserInCasestudy(user=user, casestudy=casestudy1)
        uic2 = UserInCasestudy(user=user, casestudy=casestudy2)
        uic1.save()
        uic2.save()

        sh_cat1 = StakeholderCategory(name='sc1', case_study=casestudy1)
        sh_cat2 = StakeholderCategory(name='sc1', case_study=casestudy2)
        sh_cat1.save()
        sh_cat2.save()
        sh1 = Stakeholder(name='sc1', stakeholder_category=sh_cat1)
        sh2 = Stakeholder(name='sc1', stakeholder_category=sh_cat2)
        sh1.save()
        sh2.save()

        # validate_unique is normally called when a form is validated
        strategy1_city1 = Strategy(user=uic1, coordinator=sh1, name='Stategy1')
        strategy1_city1.validate_unique()
        strategy1_city1.save()
        strategy1_city2 = Strategy(user=uic2, coordinator=sh2, name='Stategy1')
        strategy1_city2.validate_unique()
        strategy1_city2.save()
        strategy2_city1 = Strategy(user=uic1, coordinator=sh1, name='Stategy2')
        strategy2_city1.validate_unique()
        strategy2_city1.save()
        with self.assertRaisesMessage(
            ValidationError,
            'Strategy Stategy1 already exists in casestudy city1') as err:
            strategy1b_city1 = Strategy(user=uic1, coordinator=sh1,
                                        name='Stategy1')
            strategy1b_city1.validate_unique()
            strategy1b_city1.save()
        print(err.exception.message)

