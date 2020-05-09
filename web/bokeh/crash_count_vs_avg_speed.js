(() => {
    const docs_json = {
        "3b44aa3f-9433-4905-ba73-86e501c1b9a4": {
            "roots": {
                "references": [
                    {
                        "attributes": {
                            "fill_color": {
                                "value": "white"
                            },
                            "size": {
                                "units": "screen",
                                "value": 18
                            },
                            "x": {
                                "field": "x"
                            },
                            "y": {
                                "field": "y"
                            }
                        },
                        "id": "1024",
                        "type": "Circle"
                    },
                    {
                        "attributes": {
                            "fill_alpha": {
                                "value": 0.1
                            },
                            "fill_color": {
                                "value": "white"
                            },
                            "line_alpha": {
                                "value": 0.1
                            },
                            "size": {
                                "units": "screen",
                                "value": 18
                            },
                            "x": {
                                "field": "x"
                            },
                            "y": {
                                "field": "y"
                            }
                        },
                        "id": "1025",
                        "type": "Circle"
                    },
                    {
                        "attributes": {
                            "data": {
                                "x": {
                                    "__ndarray__": "AAAAAABApEAAAAAAABKwQAAAAAAAT7RAAAAAAAD4pkAAAAAAAL+5QAAAAAAAH7NAAAAAAAA6s0AAAAAAAA+4QAAAAAAAcqZAAAAAAAAGuUAAAAAAAH66QAAAAAAALLBAAAAAAABVtUAAAAAAADmxQAAAAAAAcK9AAAAAAAA+pkAAAAAAACCUQAAAAAAAO75AAAAAAABqr0AAAAAAAKqqQAAAAAAA7KhAAAAAAAC2oUAAAAAAACyzQAAAAAAAUqxAAAAAAACgnEAAAAAAAKauQAAAAAAAFJdAAAAAAABkkEAAAAAAAM6iQA==",
                                    "dtype": "float64",
                                    "shape": [
                                        29
                                    ]
                                },
                                "y": {
                                    "__ndarray__": "iH6nxbeTNECZcKs77K46QOviB3I7PDdA0dd0eW4wNEDx0V8R6d02QLPAu0YsojZA2m1PyO91NUA2ZREUM880QOU76On5qDZAui2mFkq7N0DYtrkVJr82QBDo0vzMITNAXrZOdvfFMkAPb2nzdQo4QFu1EpqovjlAGbwTT/00OEBTPqo4QYg4QH2479AFGzlAG66zXJYBOkDqwy3HaeQ5QExAdJq4rDdAx3J99ayuO0BrO+hhajk4QGeEOGgK+DhAp89v4YuKOUAc9feBGqw8QNJREsmPhTxAQGrzW+n+NEC6m4R4bikzQA==",
                                    "dtype": "float64",
                                    "shape": [
                                        29
                                    ]
                                }
                            },
                            "selected": {
                                "id": "1033"
                            },
                            "selection_policy": {
                                "id": "1034"
                            }
                        },
                        "id": "1023",
                        "type": "ColumnDataSource"
                    },
                    {
                        "attributes": {},
                        "id": "1004",
                        "type": "DataRange1d"
                    },
                    {
                        "attributes": {
                            "axis": {
                                "id": "1012"
                            },
                            "ticker": null
                        },
                        "id": "1015",
                        "type": "Grid"
                    },
                    {
                        "attributes": {},
                        "id": "1033",
                        "type": "Selection"
                    },
                    {
                        "attributes": {},
                        "id": "1010",
                        "type": "LinearScale"
                    },
                    {
                        "attributes": {},
                        "id": "1017",
                        "type": "BasicTicker"
                    },
                    {
                        "attributes": {},
                        "id": "1008",
                        "type": "LinearScale"
                    },
                    {
                        "attributes": {
                            "axis": {
                                "id": "1016"
                            },
                            "dimension": 1,
                            "ticker": null
                        },
                        "id": "1019",
                        "type": "Grid"
                    },
                    {
                        "attributes": {},
                        "id": "1029",
                        "type": "BasicTickFormatter"
                    },
                    {
                        "attributes": {},
                        "id": "1006",
                        "type": "DataRange1d"
                    },
                    {
                        "attributes": {
                            "data_source": {
                                "id": "1023"
                            },
                            "glyph": {
                                "id": "1024"
                            },
                            "hover_glyph": null,
                            "muted_glyph": null,
                            "nonselection_glyph": {
                                "id": "1025"
                            },
                            "selection_glyph": null,
                            "view": {
                                "id": "1027"
                            }
                        },
                        "id": "1026",
                        "type": "GlyphRenderer"
                    },
                    {
                        "attributes": {
                            "callback": null,
                            "tooltips": [
                                [
                                    "Region ID",
                                    "$index"
                                ],
                                [
                                    "Number of crashes",
                                    "@x"
                                ],
                                [
                                    "Avg. speed (mph)",
                                    "@y{(0.0)}"
                                ]
                            ]
                        },
                        "id": "1020",
                        "type": "HoverTool"
                    },
                    {
                        "attributes": {
                            "below": [
                                {
                                    "id": "1012"
                                }
                            ],
                            "center": [
                                {
                                    "id": "1015"
                                },
                                {
                                    "id": "1019"
                                }
                            ],
                            "left": [
                                {
                                    "id": "1016"
                                }
                            ],
                            "renderers": [
                                {
                                    "id": "1026"
                                }
                            ],
                            "title": {
                                "id": "1002"
                            },
                            "toolbar": {
                                "id": "1021"
                            },
                            "toolbar_location": null,
                            "x_range": {
                                "id": "1004"
                            },
                            "x_scale": {
                                "id": "1008"
                            },
                            "y_range": {
                                "id": "1006"
                            },
                            "y_scale": {
                                "id": "1010"
                            }
                        },
                        "id": "1001",
                        "subtype": "Figure",
                        "type": "Plot"
                    },
                    {
                        "attributes": {},
                        "id": "1031",
                        "type": "BasicTickFormatter"
                    },
                    {
                        "attributes": {
                            "text": "Number of Crashes vs Avg. Speed for All 29 Regions"
                        },
                        "id": "1002",
                        "type": "Title"
                    },
                    {
                        "attributes": {},
                        "id": "1013",
                        "type": "BasicTicker"
                    },
                    {
                        "attributes": {
                            "active_drag": "auto",
                            "active_inspect": "auto",
                            "active_multi": null,
                            "active_scroll": "auto",
                            "active_tap": "auto",
                            "tools": [
                                {
                                    "id": "1020"
                                }
                            ]
                        },
                        "id": "1021",
                        "type": "Toolbar"
                    },
                    {
                        "attributes": {
                            "axis_label": "Avg. speed",
                            "formatter": {
                                "id": "1031"
                            },
                            "ticker": {
                                "id": "1017"
                            }
                        },
                        "id": "1016",
                        "type": "LinearAxis"
                    },
                    {
                        "attributes": {},
                        "id": "1034",
                        "type": "UnionRenderers"
                    },
                    {
                        "attributes": {
                            "axis_label": "Crash count",
                            "formatter": {
                                "id": "1029"
                            },
                            "ticker": {
                                "id": "1013"
                            }
                        },
                        "id": "1012",
                        "type": "LinearAxis"
                    },
                    {
                        "attributes": {
                            "source": {
                                "id": "1023"
                            }
                        },
                        "id": "1027",
                        "type": "CDSView"
                    }
                ],
                "root_ids": [
                    "1001"
                ]
            },
            "title": "Bokeh Application",
            "version": "2.0.2"
        }
    }

    const fn = () => {
        Bokeh.safely(function () {
            (root => {
                const embed_document = root => {
                    const render_items = [{
                        "docid": "3b44aa3f-9433-4905-ba73-86e501c1b9a4",
                        "root_ids": ["1001"],
                        "roots": {"1001": "840fb949-bcca-4ab7-95a6-277f639e736e"}
                    }];
                    root.Bokeh.embed.embed_items(docs_json, render_items);
                }

                if (root.Bokeh !== undefined) {
                    embed_document(root);
                } else {
                    let attempts = 0;
                    const timer = setInterval(root => {
                        if (root.Bokeh !== undefined) {
                            clearInterval(timer);
                            embed_document(root);
                        } else {
                            attempts++;
                            if (attempts > 100) {
                                clearInterval(timer);
                                console.log("Bokeh: ERROR: Unable to run BokehJS code because BokehJS library is missing");
                            }
                        }
                    }, 10, root);
                }
            })(window);
        });
    };
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
})();
