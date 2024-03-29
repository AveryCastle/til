package com.example.hackingspringboot.reactive;

import static org.springframework.hateoas.config.EnableHypermediaSupport.HypermediaType.HAL;
import static org.springframework.hateoas.config.EnableHypermediaSupport.HypermediaType.HAL_FORMS;
import com.example.hackingspringboot.reactive.ch05.HttpTraceWrapper;
import java.net.URI;
import java.util.Map;
import org.bson.Document;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.actuate.trace.http.HttpTrace;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.convert.converter.Converter;
import org.springframework.hateoas.config.EnableHypermediaSupport;

@SpringBootApplication
@EnableHypermediaSupport(type = {HAL, HAL_FORMS})
public class HackingSpringBootCh2ReactiveApplication {

    public static void main(String[] args) {
//        BlockHound.builder()
//            .allowBlockingCallsInside(TemplateEngine.class.getCanonicalName(), "process")
//            .allowBlockingCallsInside(WebFluxLinkBuilder.class.getCanonicalName(), "linkTo")
//            .install();

        SpringApplication.run(HackingSpringBootCh2ReactiveApplication.class, args);
    }

//    @Bean
//    HttpTraceRepository traceRepository() {
//        return new InMemoryHttpTraceRepository();
//    }

//    @Bean
//    HttpTraceRepository springDataTraceRepository(HttpTraceWrapperRepository repository) {
//        return new SpringDataHttpTraceRepository(repository);
//    }

    static Converter<Document, HttpTraceWrapper> CONVERTER = //
        new Converter<Document, HttpTraceWrapper>() { //
            @Override
            public HttpTraceWrapper convert(Document document) {
                Document httpTrace = document.get("httpTrace", Document.class);
                Document request = httpTrace.get("request", Document.class);
                Document response = httpTrace.get("response", Document.class);

                return new HttpTraceWrapper(new HttpTrace( //
                    new HttpTrace.Request( //
                        request.getString("method"), //
                        URI.create(request.getString("uri")), //
                        request.get("headers", Map.class), //
                        null), new HttpTrace.Response( //
                    response.getInteger("status"), //
                    response.get("headers", Map.class)), httpTrace.getDate("timestamp").toInstant(), //
                    null, //
                    null, //
                    httpTrace.getLong("timeTaken")));
            }
        };

//    @Bean
//    public MappingMongoConverter mappingMongoConverter(MongoMappingContext context) {
//
//        MappingMongoConverter mappingConverter = //
//            new MappingMongoConverter(NoOpDbRefResolver.INSTANCE, context); // <1>
//
//        mappingConverter.setCustomConversions( // <2>
//            new MongoCustomConversions(Collections.singletonList(CONVERTER))); // <3>
//
//        return mappingConverter;
//    }
}
