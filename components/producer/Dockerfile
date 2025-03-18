FROM openjdk:21-ea-11-slim-buster

ARG PROFILE_="prod"

ENV VERSION="0.0.1-SNAPSHOT"
ENV PROFILE=$PROFILE_
# You must set these environment variables when you want to run the container.
ENV KAFKA_HOST ""
ENV SASL_USERNAME ""
ENV SASL_PASSWORD ""

COPY build/libs/publisher-$VERSION.jar .
COPY tmp/ .

CMD ["sh", "-c", "java -jar -Dspring.profiles.active=$PROFILE publisher-$VERSION.jar"]
