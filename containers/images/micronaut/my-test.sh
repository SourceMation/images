mn create-app example.micronaut.micronautguide --build=maven --lang=java
cd micronautguide
./mvnw test
./mvnw package -Dpackaging=native-image
