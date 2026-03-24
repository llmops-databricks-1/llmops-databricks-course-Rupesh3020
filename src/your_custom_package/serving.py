"""Serving endpoint configuration and helpers."""

from dataclasses import dataclass

from databricks.sdk.service.serving import (
    AiGatewayConfig,
    AiGatewayInferenceTableConfig,
    AiGatewayUsageTrackingConfig,
    EndpointCoreConfigInput,
    ServedEntityInput,
)


@dataclass
class ProvisionedEndpointConfig:
    """Configuration for a provisioned throughput endpoint."""

    endpoint_name: str = "llama-3-2-1b-provisioned"
    model_name: str = "system.ai.llama_v3_2_1b_instruct"
    model_version: str = "1"
    workload_size: str = "Small"
    scale_to_zero: bool = True
    min_provisioned_throughput: int = 0
    max_provisioned_throughput: int = 20
    catalog: str = "llmops_dev"
    schema: str = "arxiv"
    inference_table_prefix: str = "provisioned_throughput_monitoring"
    budget_policy_id: str | None = None

    def build_ai_gateway_config(self) -> AiGatewayConfig:
        """Build the AI Gateway configuration."""
        return AiGatewayConfig(
            inference_table_config=AiGatewayInferenceTableConfig(
                enabled=True,
                catalog_name=self.catalog,
                schema_name=self.schema,
                table_name_prefix=self.inference_table_prefix,
            ),
            usage_tracking_config=AiGatewayUsageTrackingConfig(
                enabled=True,
            ),
        )

    def build_endpoint_config(self) -> EndpointCoreConfigInput:
        """Build the endpoint core configuration."""
        return EndpointCoreConfigInput(
            name=self.endpoint_name,
            served_entities=[
                ServedEntityInput(
                    entity_name=self.model_name,
                    entity_version=self.model_version,
                    workload_size=self.workload_size,
                    scale_to_zero_enabled=self.scale_to_zero,
                    min_provisioned_throughput=self.min_provisioned_throughput,
                    max_provisioned_throughput=self.max_provisioned_throughput,
                )
            ],
        )
