from rest_framework import serializers
from .models import Department, Employee, Dependent


class EmployeeSerializer(serializers.ModelSerializer):
    dependents_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "email",
            "birth_date",
            "salary",
            "department",
            "dependents_count",
        ]


class DependentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        employee_id = self.context["employee_id"]
        relationship = self.validated_data["relationship"]
        employee = Employee.objects.get(pk=employee_id)

        if employee.gender == "m":
            if relationship == "husband":
                raise serializers.ValidationError(
                    "How a man can be married from a man?"
                )
            elif (
                employee.dependents.filter(relationship="wife").count() == 4
                and relationship == "wife"
            ):
                raise serializers.ValidationError(
                    "A man cannot be married from more than 4 wives."
                )
        else:
            if relationship == "wife":
                raise serializers.ValidationError(
                    "How a woman can be married from a woman?"
                )
            elif (
                employee.dependents.filter(relationship="husband").count() == 1
                and relationship == "husband"
            ):
                raise serializers.ValidationError(
                    "How a woman can be married from more than one man?"
                )

        gender = "f" if relationship in ["wife", "daughter"] else "m"
        return Dependent.objects.create(
            employee_id=employee_id,
            gender=gender,
            **validated_data,
        )

    class Meta:
        model = Dependent
        fields = ["id", "name", "gender", "birth_date", "relationship"]
        read_only_fields = ["gender"]


class UpdateDependentSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        employee_id = self.context["employee_id"]
        relationship = self.validated_data["relationship"]
        employee = Employee.objects.get(pk=employee_id)

        if employee.gender == "m":
            if relationship == "husband":
                raise serializers.ValidationError(
                    "How a man can be married from a man?"
                )
            elif (
                employee.dependents.filter(relationship="wife").count() == 4
                and relationship == "wife"
            ):
                raise serializers.ValidationError(
                    "A man cannot be married from more than 4 wives."
                )
        else:
            if relationship == "wife":
                raise serializers.ValidationError(
                    "How a woman can be married from a woman?"
                )
            elif (
                employee.dependents.filter(relationship="husband").count() == 1
                and relationship == "husband"
            ):
                raise serializers.ValidationError(
                    "How a woman can be married from more than one man?"
                )

        gender = "f" if relationship in ["wife", "daughter"] else "m"
        instance.__dict__.update(**validated_data)
        instance.gender = gender
        instance.save()
        return instance

    class Meta:
        model = Dependent
        fields = ["name", "birth_date", "relationship"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]