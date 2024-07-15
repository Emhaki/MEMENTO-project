# MEMENTO-project

### 개요
URL 단축 서비스는 긴 URL을 짧게 단축하여 사용하고, 단축된 URL을 통해 원본 URL로 리디렉션하는 기능을 제공합니다.

### **Swagger API**   



--- 

### 요구사항
**1. 필수 기능**
- **단축 URL 생성**
  - `POST /shorten`: 입력받은 긴 URL을 고유한 단축 키로 변환하고 데이터베이스에 저장.
  - 요청 본문: `{"url": "<original_url>"}`
  - 응답 본문: `{"short_url": "<shortened_url>"}`
  - **알고리즘 요구사항**:
    - 단축 키는 고유해야 하며, 중복되지 않는 키 생성.
    - 키 생성 알고리즘은 자유롭게 구현할 수 있으나 보안성과 효율성을 고려해야 함.
  
- **원본 URL 리디렉션**
  - `GET /<short_key>`: 단축된 키를 통해 원본 URL로 리디렉션.
  - 응답:
    - 키가 존재하면 301 상태 코드로 원본 URL로 리디렉션.
    - 키가 존재하지 않으면 404 상태 코드로 오류 메시지 반환.

## **수행 내역(Description)**

### 1-1 **단축 URL 생성**
<img src="MEMENTO/img/shorten2.png" alt="Swagger API" width="300">  

- 요청 본문: {"url": "<original_url>"}
- 응답 본문: {"short_url": "<shortened_url>"}

- 과제 수행 내역
<img src="/Users/emhaki/Desktop/MEMENTO/img/shorten_response.png" alt="Swagger API" width="300">

    - string.ascii_letters + string.digits를 사용하여 문자, 숫자 조합
    - length를 통해 문자열 길이 쉽게 조정 가능
    - 단축 URL 중복값이 있다면 DB에 저장하지 않고 재생성
    - 만료 기간은 선택적으로 추가 가능하도록 구현

### 1-2 **원본 URL 리디렉션**

<img src="/Users/emhaki/Desktop/MEMENTO/img/redirection.png" alt="Swagger API" width="300">

- 과제 수행 내역
    - <img src="/Users/emhaki/Desktop/MEMENTO/img/redirection2.png" alt="Swagger API" width="300">
    - 단축키 입력시 원본 URL 리디렉션
    - <img src="/Users/emhaki/Desktop/MEMENTO/img/redirection_404.png" alt="Swagger API" width="300">
    - 키가 존재하지 않으면 404 반환
    - <img src="/Users/emhaki/Desktop/MEMENTO/img/success.png" alt="Swagger API" width="300">
    - 키가 존재하면 원본 URL 반환
    
----

**2. 추가 요구사항**
- **데이터베이스**: 원본 URL과 단축 키 매핑을 저장하기 위한 데이터베이스 사용. (여러 개의 데이터베이스를 혼합적으로 사용해도 됨)
  - SQLite, PostgreSQL, MongoDB, Redis 등 자유롭게 선택 가능.
  - 단, 확장성과 애플리케이션의 특성, 관리의 용이성을 종합적으로 고려해서 가장 적절한 데이터베이스(들)를 선택하여야 하고, 그 사유를 간략히 과제 제출 시 기재. 유저의 수가 많아질 수 있음을 반드시 고려해서 DB 스택을 설계해야함.

- MySQL 선택 이유
    - 수평적 확장이 용이하며 여러 노드에 데이터를 분산시켜 처리할 수 있기 때문에 대규모 사용자 트래픽을 효과적으로 처리할 수 있음
    - 클러스터링 및 분산 데이터베이스 시스템은 대규모 데이터와 사용자 요청을 처리하는데 적합하다고 판단
    - MySQL은 오픈 소스 소프트웨어로 커뮤니티 지원을 받을 수 있으며, 풍부한 리소스와 문서 등을 통해 다양한 문제 해결에 도움이 될 수 있음


- **문서화**: 작성한 API에 대한 Swagger 문서 생성.
<img src="MEMENTO/img/swagger.png" alt="Swagger API" width="300">

```python
{
   "openapi":"3.1.0",
   "info":{
      "title":"FastAPI",
      "version":"0.1.0"
   },
   "paths":{
      "/shorten":{
         "post":{
            "summary":"Shorten Url",
            "operationId":"shorten_url_shorten_post",
            "parameters":[
               {
                  "name":"url",
                  "in":"query",
                  "required":true,
                  "schema":{
                     "type":"string",
                     "title":"Url"
                  }
               },
               {
                  "name":"expiration_time",
                  "in":"query",
                  "required":false,
                  "schema":{
                     "type":"integer",
                     "title":"Expiration Time"
                  }
               }
            ],
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/URLResponse"
                        }
                     }
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            }
         }
      },
      "/{short_key}":{
         "get":{
            "summary":"Redirect Original Url",
            "operationId":"redirect_original_url__short_key__get",
            "parameters":[
               {
                  "name":"short_key",
                  "in":"path",
                  "required":true,
                  "schema":{
                     "type":"string",
                     "title":"Short Key"
                  }
               }
            ],
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           
                        }
                     }
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            }
         }
      },
      "/stats/{short_key}":{
         "get":{
            "summary":"Get Status",
            "operationId":"get_status_stats__short_key__get",
            "parameters":[
               {
                  "name":"short_key",
                  "in":"path",
                  "required":true,
                  "schema":{
                     "type":"string",
                     "title":"Short Key"
                  }
               }
            ],
            "responses":{
               "200":{
                  "description":"Successful Response",
                  "content":{
                     "application/json":{
                        "schema":{
                           
                        }
                     }
                  }
               },
               "422":{
                  "description":"Validation Error",
                  "content":{
                     "application/json":{
                        "schema":{
                           "$ref":"#/components/schemas/HTTPValidationError"
                        }
                     }
                  }
               }
            }
         }
      }
   },
   "components":{
      "schemas":{
         "HTTPValidationError":{
            "properties":{
               "detail":{
                  "items":{
                     "$ref":"#/components/schemas/ValidationError"
                  },
                  "type":"array",
                  "title":"Detail"
               }
            },
            "type":"object",
            "title":"HTTPValidationError"
         },
         "URLResponse":{
            "properties":{
               "short_url":{
                  "type":"string",
                  "title":"Short Url"
               }
            },
            "type":"object",
            "required":[
               "short_url"
            ],
            "title":"URLResponse"
         },
         "ValidationError":{
            "properties":{
               "loc":{
                  "items":{
                     "anyOf":[
                        {
                           "type":"string"
                        },
                        {
                           "type":"integer"
                        }
                     ]
                  },
                  "type":"array",
                  "title":"Location"
               },
               "msg":{
                  "type":"string",
                  "title":"Message"
               },
               "type":{
                  "type":"string",
                  "title":"Error Type"
               }
            },
            "type":"object",
            "required":[
               "loc",
               "msg",
               "type"
            ],
            "title":"ValidationError"
         }
      }
   }
}
  ```

### 보너스 기능 (각 기능 구현 시 가산점)
**1. URL 키 만료 기능**
- 키 생성 시 만료 기간을 지정할 수 있으며, 만료된 키는 삭제 처리.
- `POST /shorten`: 요청 본문에 만료 기간을 선택적으로 추가할 수 있어야 함.

<img src="/Users/emhaki/Desktop/MEMENTO/img/shorten2.png" alt="Swagger API" width="300">
<img src="/Users/emhaki/Desktop/MEMENTO/img/expires.png" alt="Swagger API" width="300">
<img src="/Users/emhaki/Desktop/MEMENTO/img/delete.png" alt="Swagger API" width="300">

- 만료기간 설정한 후 만료시간이 지난 키는 스케줄러를 이용해 삭제 처리

**2. 통계 기능**
- 각 단축 키의 조회 수를 추적하고 이를 반환하는 통계 엔드포인트 추가.
- `GET /stats/<short_key>`: 해당 키의 조회 수 반환.
<img src="/Users/emhaki/Desktop/MEMENTO/img/count.png" alt="Swagger API" width="300">
- 단축 키의 조회 횟수를 DB에 저장하고 반환 stats/<short_key> 앤드포인트를 통해 반환

**3. 테스트 코드**
- 단위 테스트 및 통합 테스트 코드 포함.